FROM nginx:alpine

COPY . /usr/share/nginx/html/

RUN printf 'server {\n\
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
    # novel.md specifically — force text/markdown so gzip triggers\n\
    location = /novel.md {\n\
        default_type "text/markdown; charset=utf-8";\n\
        add_header Cache-Control "public, max-age=0, must-revalidate";\n\
    }\n\
\n\
    # html / md catch-all: always revalidate\n\
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
