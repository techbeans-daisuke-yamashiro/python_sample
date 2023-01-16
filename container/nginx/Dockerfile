FROM nginx:1.23-alpine
WORKDIR '/etc/nginx'
RUN rm conf.d/default.conf
COPY ./container/nginx/nginx.conf /etc/nginx/
COPY ./container/nginx/fastapi.conf /etc/nginx/conf.d
