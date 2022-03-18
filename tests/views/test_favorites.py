from http import HTTPStatus
from random import choice, randint

import pytest


class TestFavoritesView:
    url = "/favorites/movies/"

    @pytest.fixture
    def favorites_movies(self, db, user, movies):
        for movie in movies:
            user.favorites.append(movie)
        db.session.commit()

    def test_unauthorized(self, client):
        assert client.get(self.url).status_code == HTTPStatus.UNAUTHORIZED

    def test_get_favorites_success(
        self, user, client, movies, favorites_movies, login_headers
    ):
        response = client.get(self.url, headers=login_headers)
        assert response.status_code == HTTPStatus.OK
        assert len(response.json) == 10


class TestManageFavoriteView:
    url = "/favorites/movies/{movie_id}/"

    def test_unauthorized(self, client):
        assert client.post(self.url.format(movie_id=randint(1, 100))).status_code == 401
        assert client.delete(self.url.format(movie_id=randint(1, 100))).status_code == 401

    def test_movie_not_found(self, user, client, login_headers):
        assert client.post(self.url.format(movie_id=1), headers=login_headers).status_code == 404
        assert client.delete(
            self.url.format(movie_id=1), headers=login_headers
        ).status_code == 404

    def test_add_movie_to_favorites(self, user, client, movies, login_headers):
        movie = choice(movies)
        response = client.post(self.url.format(movie_id=movie.id), headers=login_headers)
        assert response.status_code == HTTPStatus.OK
        assert response.json is None
        assert movie in user.favorites

    def test_delete_movie_from_favorites(self, user, client, movies, login_headers):
        movie = choice(movies)
        user.favorites.append(movie)

        response = client.delete(
            self.url.format(movie_id=movie.id), headers=login_headers
        )
        assert response.status_code == 204
        assert movie not in user.favorites
