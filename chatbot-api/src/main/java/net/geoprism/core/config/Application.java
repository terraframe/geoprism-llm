package net.geoprism.core.config;

import org.springframework.context.annotation.AnnotationConfigApplicationContext;
import org.springframework.context.support.AbstractApplicationContext;

public class Application
{

  public static void main(String[] args)
  {
    try (AbstractApplicationContext context = new AnnotationConfigApplicationContext(CoreConfiguration.class))
    {
      context.registerShutdownHook();
      context.start();
      context.stop();
    }
  }
}
