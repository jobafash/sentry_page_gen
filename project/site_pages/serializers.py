from rest_framework import serializers
from site_pages.models import Page, MetaTag, CSS, ScriptTag
from django.contrib.auth.models import User



class MetaTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaTag
        exclude = ['page']

class ScriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScriptTag
        exclude = ['page']
 
class CSSSerializer(serializers.ModelSerializer):
    class Meta:
        model = CSS
        exclude = ['page']


class PageSerializer(serializers.ModelSerializer):
    meta_tags = MetaTagSerializer(many=True)
    scripts = ScriptSerializer(many=True)
    css = CSSSerializer(many=True)
    lookup_field = 'slug'
    class Meta:
        model = Page
        fields = '__all__'
        read_only_fields = ['slug']


    def create(self, validated_data):
        meta_tag_data = validated_data.pop('meta_tags')
        script_data = validated_data.pop('scripts')
        css_data = validated_data.pop('css')
        page = Page.objects.create(**validated_data)

        for data in meta_tag_data:
            MetaTag.objects.create(page=page, **data)
        
        for data in script_data:
            print(data)
            ScriptTag.objects.create(page=page, **data)
        
        for data in css_data:
            CSS.objects.create(page=page, **data)
            
        return page


class PageUpdateSerializer(serializers.ModelSerializer):
    lookup_field = 'slug'
    class Meta:
        model = Page
        fields = ['content']


class RegisterSerialiazer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user