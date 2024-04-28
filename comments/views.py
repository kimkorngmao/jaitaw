from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import *

# Create your views here.

class CreateCommentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = CommentSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response({ "created_comment": "Created comment succesfully." }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetailAPIView(APIView):
    def get(self, request, id, format=None):
        comment = get_object_or_404(Comment, id=id)
        serializer = CommentSerializer(comment, context={'request': request})
        return Response({ "comment": serializer.data }, status=status.HTTP_200_OK)

class CommentUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, id, format=None):
        comment = get_object_or_404(Comment, id=id)
        if comment.author.username == request.user.username:
            serializer = CommentSerializer(comment, data=request.data, context={'request': request}, partial=True)
            if serializer.is_valid():
                # Update comment properties with validated data
                comment.content = serializer.validated_data.get('content', comment.content)  # Update content if provided
                # Update other fields as needed
                comment.save()
                return Response({ "updated_comment": serializer.data }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id, format=None):
        comment = get_object_or_404(Comment, id=id)
        if comment.author.username == request.user.username or comment.post.author.username == request.user.username:
            comment.delete()
            return Response({ "message": "Comment deleted successfully!" }, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({ "message": "You do not have permission to delete this comment!" }, status=status.HTTP_403_FORBIDDEN) 

class CommentsByPostAPIListView(APIView):
    def remove_duplicates(self, input_list):
        unique_list = []
        for item in input_list:
            if item not in unique_list:
                unique_list.append(item)
        return unique_list

    def get(self, request, post_code):
        try:
            comment_request_id = request.query_params.get('comment')
            post = get_object_or_404(Post, code=post_code)

            current_user_comments = []
            if request.user.is_authenticated:
                current_user_comments = Comment.objects.filter(author=request.user, post=post)

            comment = Comment.objects.filter(id=comment_request_id, post=post)
            comments = Comment.objects.filter(post=post)
            
            all_comments = self.remove_duplicates(list(comment) + list(current_user_comments) + list(comments))
            serializer = CommentSerializer(all_comments, many=True, context={'request': request})
            return Response({'comments': serializer.data})
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    
class CommentLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        comment = get_object_or_404(Comment, id=id)
        user = request.user
        like_comment = CommentLike.objects.filter(user=user, comment=comment)

        if like_comment.exists():
            like_comment.delete()
            message = f"You have unlike {comment.content}."
        else:
            CommentLike.objects.create(user=user, comment=comment)
            message = f"You are now like {comment.content}."
       
        return Response({"message": message}, status=status.HTTP_200_OK)