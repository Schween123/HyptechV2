from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import RPi.GPIO as GPIO
import time

from ..models import Owner, BoardingHouse, Room, Tenant, Guardian, Transaction, FaceImage
from .serializers import OwnerSerializer, BoardingHouseSerializer, RoomSerializer, TenantSerializer, GuardianSerializer, TransactionSerializer, FaceImageSerializer

class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer

class BoardingHouseViewSet(viewsets.ModelViewSet):
    queryset = BoardingHouse.objects.all()
    serializer_class = BoardingHouseSerializer

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer

class GuardianViewSet(viewsets.ModelViewSet):
    queryset = Guardian.objects.all()
    serializer_class = GuardianSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class FaceImageViewSet(viewsets.ModelViewSet):
    queryset = FaceImage.objects.all()
    serializer_class = FaceImageSerializer

class BillAcceptorView(APIView):
    billAcceptorPin = 7  # Physical Pin 7 (GPIO4)
    ledPin = 13          # Physical Pin 13 (GPIO27)
    inhibitPin = 11      # Physical Pin 11 (GPIO17)
    pulseDtct = 0        # Counter for consecutive pulses
    lastPulseTime = 0    # Stores the time when the last pulse was detected
    pulseDelay = 0.5     # Maximum delay between pulses in seconds

    def setup_gpio(self):
        GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
        GPIO.setup(self.billAcceptorPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set the bill acceptor pin as input with pull-up resistor
        GPIO.setup(self.ledPin, GPIO.OUT)  # Set the LED pin as output
        GPIO.setup(self.inhibitPin, GPIO.OUT)  # Set the inhibit pin as output
        GPIO.output(self.ledPin, GPIO.LOW)
        GPIO.output(self.inhibitPin, GPIO.LOW)

    def detect_bill(self):
        start_time = time.time()
        bill_value = 0
        pulse_detected = False

        while time.time() - start_time < 30:  # Poll for up to 30 seconds
            pinState = GPIO.input(self.billAcceptorPin)
            currentTime = time.time()

            if pinState == GPIO.LOW:
                GPIO.output(self.ledPin, GPIO.HIGH)

                if currentTime - self.lastPulseTime <= self.pulseDelay:
                    self.pulseDtct += 1
                else:
                    self.pulseDtct = 1

                self.lastPulseTime = currentTime
                pulse_detected = True

            else:
                GPIO.output(self.ledPin, GPIO.LOW)

            # Once a pulse sequence is detected, return the corresponding bill value
            if pulse_detected and (currentTime - self.lastPulseTime > self.pulseDelay):
                if self.pulseDtct == 10:
                    bill_value = 100
                elif self.pulseDtct == 2:
                    bill_value = 20
                elif self.pulseDtct == 5:
                    bill_value = 50
                elif self.pulseDtct == 20:
                    bill_value = 200
                elif self.pulseDtct == 50:
                    bill_value = 500
                elif self.pulseDtct == 100:
                    bill_value = 1000

                break  # Exit the loop once a valid pulse sequence is detected

            time.sleep(0.05)  # Short delay to prevent excessive CPU usage

        self.pulseDtct = 0  # Reset pulse count after detection
        return bill_value

    def get(self, request, format=None):
        try:
            self.setup_gpio()  # Ensure GPIO is set up before any operations
            bill_value = self.detect_bill()
            GPIO.cleanup()
            return Response({'bill_value': bill_value}, status=status.HTTP_200_OK)
        except Exception as e:
            GPIO.cleanup()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#
class UltrasonicSensorView(APIView):
    def initialize_gpio(self):
        GPIO.setmode(GPIO.BCM)  # Use BCM mode for GPIO numbering
        
        # Set GPIO Pins
        self.GPIO_TRIGGER = 23
        self.GPIO_ECHO = 24
        
        # Set GPIO direction (IN / OUT)
        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)
    
    def get_distance(self):
        # Set Trigger to HIGH
        GPIO.output(self.GPIO_TRIGGER, True)

        # Set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.GPIO_TRIGGER, False)

        start_time = time.time()
        stop_time = time.time()

        # Save start time
        while GPIO.input(self.GPIO_ECHO) == 0:
            start_time = time.time()

        # Save time of arrival
        while GPIO.input(self.GPIO_ECHO) == 1:
            stop_time = time.time()

        # Time difference between start and arrival
        time_elapsed = stop_time - start_time
        # Multiply with the speed of sound (34300 cm/s)
        # and divide by 2, because there and back
        distance = (time_elapsed * 34300) / 2

        return distance

    def get(self, request, format=None):
        try:
            self.initialize_gpio()
            distance = self.get_distance()
        finally:
            GPIO.cleanup()  # Ensure GPIO is always cleaned up
        return Response({'distance': distance}, status=status.HTTP_200_OK)
