FROM nginx:1.23-alpine
WORKDIR '/etc/nginx'
RUN rm conf.d/default.conf
COPY ./docker/nginx/nginx.conf /etc/nginx/
COPY ./docker/nginx/fastapi.conf /etc/nginx/conf.d
