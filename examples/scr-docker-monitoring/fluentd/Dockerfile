FROM fluent/fluentd:v1.12.0-debian-1.0
USER root
RUN ["gem", "install", "elasticsearch", "--no-document", "--version", "7.17.0"]
RUN ["gem", "install", "fluent-plugin-elasticsearch", "--no-document"]
USER fluent
