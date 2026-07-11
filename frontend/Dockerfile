FROM nginxinc/nginx-unprivileged:1.27-alpine

WORKDIR /usr/share/nginx/html

USER root

RUN chown -R nginx:0 /usr/share/nginx/html && \
    chmod -R g+rwx /usr/share/nginx/html

COPY index.html app.js style.css ./
COPY nginx.conf /etc/nginx/conf.d/default.conf

USER nginx

EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]