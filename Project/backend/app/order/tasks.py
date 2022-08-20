from asgiref.sync import async_to_sync
from celery import shared_task
from celery.utils.log import get_task_logger
from channels.layers import get_channel_layer
from django.utils import timezone

from order.constants import OrderApprovedType, OrderToClientType, PointSourceType, OrderAtClientType, \
    OrderDeliveredType, PointDestinationType
from order.models import Order, Point
from robot.models import Robot

logger = get_task_logger(__name__)


@shared_task
def send_order_to_robot():
    robots = Robot.objects.all()
    for robot in robots:
        if robot.is_active and robot.is_available:
            order = Order.objects.filter(status=OrderApprovedType).order_by('created_at').first()

            if order:
                notify_robot(order, PointDestinationType, robot)

                robot.is_available = False
                robot.save()

                order.status = OrderToClientType
                order.save()


def notify_robot(order, point_type, robot=None):
    if not robot:
        robot = Robot.objects.first()

    source_point = Point.objects.filter(point_type=PointSourceType).first()

    async_to_sync(get_channel_layer().group_send)(
        robot.title,
        {
            'type': 'bot_message',
            'message': {
                'order_id': order.id,
                'source_point_x': source_point.longitude,
                'source_point_y': source_point.latitude,
                'destination_point_x': order.destination.longitude,
                'destination_point_y': order.destination.latitude,
                'point_type': point_type
            }
        }
    )


@shared_task
def auto_deliver_orders():
    logger.info("Auto delivering orders ...")
    orders = Order.objects.filter(status=OrderAtClientType)

    for order in orders:
        on_destination_time_max = order.on_destination_time + timezone.timedelta(minutes=2)
        if timezone.now() > on_destination_time_max:
            notify_robot(order, PointSourceType)

            order.status = OrderDeliveredType
            order.save()

