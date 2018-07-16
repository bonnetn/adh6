DIR=$(dirname "$0")
rm -r "$DIR/src/app/api"
wget http://central.maven.org/maven2/io/swagger/swagger-codegen-cli/2.3.1/swagger-codegen-cli-2.3.1.jar -O swagger-codegen-cli.jar
java -jar swagger-codegen-cli.jar generate -i "$DIR/swagger.yaml" -l typescript-angular -o "$DIR/src/app/api" --additional-properties ngVersion=6
rm swagger-codegen-cli.jar
