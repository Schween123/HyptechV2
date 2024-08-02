from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import OwnerViewSet, BoardingHouseViewSet, RoomViewSet, TenantViewSet, GuardianViewSet, TransactionViewSet, FaceImageViewSet, BillAcceptorView, UltrasonicSensorView

router = DefaultRouter()
router.register(r'owners', OwnerViewSet)
router.register(r'boardinghouses', BoardingHouseViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'tenants', TenantViewSet)
router.register(r'guardians', GuardianViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'faceimages', FaceImageViewSet)

# Include the router URLs
urlpatterns = router.urls

# Add the custom URL pattern for BillAcceptorView
urlpatterns += [
    path('bill-acceptor/', BillAcceptorView.as_view(), name='bill_acceptor'),
    path('sensor/', UltrasonicSensorView.as_view(), name='sensor_data'),
]