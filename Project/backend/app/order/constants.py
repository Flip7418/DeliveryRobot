OrderPillType = 'pill'
OrderSimptomType = 'simptom'

OrderTypes = (
    (OrderPillType, 'С таблеткой'),
    (OrderSimptomType, 'С симптомом'),
)

OrderModerationType = 'on_moderation'
OrderDeclinedType = 'declined'
OrderApprovedType = 'approved_and_on_queue'
OrderToClientType = 'going_to_client'
OrderAtClientType = 'at_client'
OrderDeliveredType = 'delivered'

OrderStatuses = (
    (OrderModerationType, 'В модерации'),
    (OrderDeclinedType, 'Отклонено'),
    (OrderApprovedType, 'Подтвержден и в очереди'),
    (OrderToClientType, 'На пути к клиенту'),
    (OrderAtClientType, 'У клиента'),
    (OrderDeliveredType, 'Доставлено'),
)

ActiveStatuses = [OrderModerationType, OrderApprovedType, OrderToClientType,
                  OrderAtClientType]
FinishedStatuses = [OrderDeclinedType, OrderDeliveredType]

PointSourceType = 'source'
PointDestinationType = 'destination'

PointTypes = (
    (PointSourceType, 'Источник'),
    (PointDestinationType, 'Назначение'),
)
