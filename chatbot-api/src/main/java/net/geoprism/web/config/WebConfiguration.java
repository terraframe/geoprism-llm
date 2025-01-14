package net.geoprism.web.config;

import java.util.List;
import java.util.concurrent.Executor;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.aop.interceptor.AsyncUncaughtExceptionHandler;
import org.springframework.aop.interceptor.SimpleAsyncUncaughtExceptionHandler;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.converter.HttpMessageConverter;
import org.springframework.http.converter.json.MappingJackson2HttpMessageConverter;
import org.springframework.scheduling.annotation.AsyncConfigurer;
import org.springframework.scheduling.concurrent.ConcurrentTaskExecutor;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;
import org.springframework.web.servlet.config.annotation.AsyncSupportConfigurer;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebConfiguration implements WebMvcConfigurer, AsyncConfigurer
{
  private static final Logger logger = LoggerFactory.getLogger(WebConfiguration.class);

  @Override
  public void addCorsMappings(CorsRegistry registry)
  {
    registry.addMapping("/**").allowedOrigins("*");
  }

  @Override
  @Bean(name = "taskExecutor")
  public Executor getAsyncExecutor()
  {
    logger.debug("Creating Async Task Executor");

    ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
    executor.setCorePoolSize(2);
    executor.setMaxPoolSize(10);
    executor.setQueueCapacity(1000);
    executor.setThreadNamePrefix("async");
    return executor;
  }

  // ---------------> Use this task executor also for async rest methods
  @Bean
  protected WebMvcConfigurer webMvcConfigurer()
  {
    return new WebMvcConfigurer()
    {
      @Override
      public void configureAsyncSupport(AsyncSupportConfigurer configurer)
      {
        configurer.setTaskExecutor(getTaskExecutor());
      }
    };
  }

  @Bean
  protected ConcurrentTaskExecutor getTaskExecutor()
  {
    return new ConcurrentTaskExecutor(this.getAsyncExecutor());
  }

  @Override
  public AsyncUncaughtExceptionHandler getAsyncUncaughtExceptionHandler()
  {
    return new SimpleAsyncUncaughtExceptionHandler();
  }

  @Override
  public void configureMessageConverters(List<HttpMessageConverter<?>> converters)
  {
    converters.add(new MappingJackson2HttpMessageConverter());
  }
}