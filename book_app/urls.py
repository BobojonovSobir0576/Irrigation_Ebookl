from django.urls import path
from book_app import views


urlpatterns = [
    path('<int:cate_id>/',views.BookList.as_view()),
    path('download/<int:id>/',views.DownloadBooksViews.as_view()),
    path('<int:id/',views.BookDetailViews.as_view()),
    path('filter/',views.BookingsListView.as_view()),
    # path('filter_search/',views.BookFilterViews.as_view()),
    path('count_cate/',views.CategoriesCountView.as_view()),
    path('get_download/',views.GetBookDownloadViews.as_view()),
    path('create_book/',views.CreateBook.as_view()),
    path('create_post/',views.CreatePostViews.as_view()),
]