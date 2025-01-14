package net.geoprism.core.config;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.env.Environment;
import org.springframework.stereotype.Service;

import software.amazon.awssdk.regions.Region;

@Service
public class AppProperties
{
  @Autowired
  private Environment env;

  public String getAgentId()
  {
    return env.getProperty("bedrock.agent.id");
  }

  public String getAgentAliasId()
  {
    return env.getProperty("bedrock.agent.alias.id");
  }

  public Region getRegion()
  {
    return Region.of(env.getProperty("bedrock.region"));
  }

  public String getAccessKeyId()
  {
    return env.getProperty("access.key.id");
  }

  public String getSecretAccessKey()
  {
    return env.getProperty("secret.access.key");
  }

}
