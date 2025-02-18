package net.geoprism.core.service;

import java.util.UUID;

import org.junit.Assert;
import org.junit.Ignore;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit.jupiter.SpringExtension;

import net.geoprism.core.config.TestConfiguration;
import net.geoprism.core.model.Message;

@ExtendWith(SpringExtension.class)
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.MOCK, classes = TestConfiguration.class)
@AutoConfigureMockMvc
public class BedrockServiceIntegrationTest
{

  @Autowired
  private BedrockService service;

  // write test cases here
  @Test
  @Ignore
  public void test()
  {
    String sessionId = UUID.randomUUID().toString();
    String inputText = "What school zones are impacted by reach_25 flooding?";

//    Message message = service.prompt(sessionId, inputText);
//
//    System.out.println(message.getContent());
//
//    Assert.assertTrue(message.getContent().trim().length() > 0);
  }
}