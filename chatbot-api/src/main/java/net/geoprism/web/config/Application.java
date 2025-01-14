package net.geoprism.web.config;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.web.servlet.support.SpringBootServletInitializer;
import org.springframework.context.annotation.ComponentScan;

@SpringBootApplication
@ComponentScan(basePackages = { "net.geoprism.core", "net.geoprism.web" })
public class Application extends SpringBootServletInitializer
{
  public static void main(String[] args)
  {
    SpringApplication.run(Application.class, args);
  }
}
