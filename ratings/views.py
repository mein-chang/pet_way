from .serializers import RatingPetSerializer, RatingProviderSerializer
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from .models import Rating
from orders.models import Order


# provider avaliando o pet/dono do pet
class RatingPetView(APIView):
    def patch(self,request,order_id):
        try:
            order = Order.objects.get(id=order_id)

            if not order.completed:
                return Response({"message": "wait until the order is completed"},status=status.HTTP_400_BAD_REQUEST)

            if order.rating:
                serializer = RatingPetSerializer(order.rating,data=request.data)
                
                if not serializer.is_valid():
                    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

                serializer.save()

                return Response(serializer.data)
            else:
                request.data["customer_rating"] = 0
                serializer = RatingPetSerializer(data=request.data)

                if not serializer.is_valid():
                    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
                
                rating = Rating.objects.create(**serializer.validated_data)

                order.rating = rating
                order.save()

                serializer = RatingPetSerializer(rating)

                return Response(serializer.data,status=status.HTTP_201_CREATED)
                
        except ObjectDoesNotExist:
             return Response({ "message": "Order not found!"},status=status.HTTP_404_NOT_FOUND)

       
# customer avaliando o provider
class RatingProviderView(APIView):
    def patch(self,request,order_id):
        try:
            order = Order.objects.get(id=order_id)
            
            if not order.completed:
                return Response({"message": "wait until the order is completed"},status=status.HTTP_400_BAD_REQUEST)

            if order.rating:
                serializer = RatingProviderSerializer(order.rating,data=request.data)
                
                if not serializer.is_valid():
                    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

                serializer.save()

                return Response(serializer.data)
            else:
                request.data["provider_rating"] = 0
                serializer = RatingProviderSerializer(data=request.data)

                if not serializer.is_valid():
                    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
                
                rating = Rating.objects.create(**serializer.validated_data)

                order.rating = rating
                order.save()

                serializer = RatingProviderSerializer(rating)

                return Response(serializer.data,status=status.HTTP_201_CREATED)
                
        except ObjectDoesNotExist:
             return Response({ "message": "Order not found!"},status=status.HTTP_404_NOT_FOUND)
