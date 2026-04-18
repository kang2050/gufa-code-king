FROM nginx:alpine

COPY . /usr/share/nginx/html/

RUN printf 'types {\n\
    text/html                             html htm;\n\
    text/css                              css;\n\
    text/plain                            txt;\n\
    text/markdown                         md;\n\
    application/javascript                js;\n\
    application/json                      json;\n\
    image/jpeg                            jpg jpeg;\n\
    image/png                             png;\n\
    image/webp                            webp;\n\
    image/svg+xml                         svg;\n\
    image/x-icon                          ico;\n\
    font/woff                             woff;\n\
    font/woff2                            woff2;\n\
}\n\
default_type application/octet-stream;\n\
\n\
server {\n\
    listen 80;\n\
    server_name _;\n\
    root /usr/share/nginx/html;\n\
    index index.html;\n\
    client_max_body_size 50M;\n\
\n\
    # jpg / webp / png: long cache\n\
    location ~* \\.(jpg|jpeg|png|webp|avif|svg|ico|woff2?)$ {\n\
        expires 30d;\n\
        add_header Cache-Control "public, max-age=2592000, immutable";\n\
        access_log off;\n\
    }\n\
\n\
    # html / md: always revalidate\n\
    location ~* \\.(html|md)$ {\n\
        add_header Cache-Control "public, max-age=0, must-revalidate";\n\
    }\n\
\n\
    location / {\n\
        try_files $uri $uri/ /index.html;\n\
    }\n\
\n\
    gzip on;\n\
    gzip_comp_level 6;\n\
    gzip_types text/plain text/markdown text/css application/javascript application/json image/svg+xml text/html;\n\
    gzip_min_length 512;\n\
    gzip_vary on;\n\
}\n' > /etc/nginx/conf.d/default.conf

EXPOSE 80
