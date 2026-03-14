FROM eclipse-temurin:17-jre

WORKDIR /app

COPY java/target/mathutils-java-1.0-SNAPSHOT.jar app.jar

EXPOSE 8080

CMD ["sh", "-c", "java -jar app.jar; echo App exited; sleep 3600"]
