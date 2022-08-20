from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import sync_to_async
from django.utils import timezone

from order.constants import PointDestinationType, PointSourceType, OrderAtClientType, \
    OrderDeclinedType
from order.models import Order, Point
from robot.models.robot import Robot


class OrderConsumer(AsyncWebsocketConsumer):
    room_group_name = None

    async def connect(self):
        self.room_group_name = self.scope['url_route']['kwargs']['robot_title']

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        await self.change_robot_status(True, True)

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

            await self.change_robot_status(False, False)
        else:
            pass

    # Receive message for bot and send it to bot
    async def bot_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        order_id = text_data_json['order_id']
        point_type = text_data_json['point_type']
        is_finished = text_data_json['is_finished']

        source_point = await self.get_source_point()
        if point_type == PointDestinationType:
            if is_finished:
                await self.update_order_status(order_id, OrderAtClientType)
                await self.update_order_on_destination_time(order_id)
                await self.change_robot_status(True, False)
            else:
                await self.update_order_status(order_id, OrderDeclinedType)
                await self.send_robot_to_source(source_point)
                await self.change_robot_status(True, False)
        elif point_type == PointSourceType:
            if is_finished:
                await self.change_robot_status(True, True)
            else:
                await self.send_robot_to_source(source_point)
                await self.change_robot_status(True, False)

    @sync_to_async
    def change_robot_status(self, is_active, is_available):
        robot, _ = Robot.objects.get_or_create(title=self.room_group_name)
        robot.is_active = is_active
        robot.is_available = is_available
        robot.save()

    @sync_to_async
    def update_order_status(self, order_id, status):
        order = Order.objects.get(id=order_id)
        order.status = status
        order.save()

    @sync_to_async
    def update_order_on_destination_time(self, order_id):
        order = Order.objects.get(id=order_id)
        order.on_destination_time = timezone.now()
        order.save()

    @sync_to_async
    def get_source_point(self):
        return Point.objects.get(point_type=PointSourceType)

    async def send_robot_to_source(self, point):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'bot_message',
                'message': {
                    'order_id': None,
                    'point_x': point.longitude,
                    'point_y': point.latitude,
                    'point_type': point.point_type
                }
            }
        )
