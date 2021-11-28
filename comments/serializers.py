from rest_framework import serializers

from comments.models import Comment

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['created_at', 'content', 'image', 'author' ]
        read_only_fields = ['creation_at',  ]