from rest_framework import serializers
from .models import Rating

class RatingPetSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Rating
        fields = "__all__"
        extra_kwargs = {"id":{'read_only':True},"customer_comment":{'required':False},"provider_comment":{'required':False},"customer_rating":{'required':False}, "provider_rating":{"max_value":5, "min_value":0}}

    def update(self,instance,validated_data):
        instance.provider_rating = validated_data.get('provider_rating',instance.provider_rating)
        instance.provider_comment = validated_data.get('provider_comment',instance.provider_comment)
        instance.save()

        return instance

    

class RatingProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = "__all__"
        extra_kwargs = {"id":{'read_only':True},"customer_comment":{'required':False},"provider_comment":{'required':False},"provider_rating":{'required':False}, "customer_rating":{"max_value":5, "min_value":0}}
    
    def update(self,instance,validated_data):
        instance.customer_rating = validated_data.get('customer_rating',instance.customer_rating)
        instance.customer_comment = validated_data.get('customer_comment',instance.customer_comment)
        instance.save()

        return instance
   