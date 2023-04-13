from rest_framework import serializers

from reviews.models import Review, Title

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')
    title = serializers.PrimaryKeyRelatedField(queryset=Title.objects.all(), write_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'title', 'score', 'pub_date')
        model = Review
