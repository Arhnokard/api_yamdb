from rest_framework import serializers

from reviews.models import Comment, Review, Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')
    title = serializers.PrimaryKeyRelatedField(queryset=Title.objects.all(),
                                               write_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'title', 'score', 'pub_date')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field='username')
    rewiew = serializers.PrimaryKeyRelatedField(queryset=Review.objects.all(),
                                               write_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'review', 'pub_date')
        model = Comment
