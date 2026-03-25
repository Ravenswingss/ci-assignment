package com.example.springjavaapp;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class HelloControllerTest {

    @Test
    void testHello() {
        HelloController controller = new HelloController();
        String response = controller.hello();
        assertEquals("Hello from Spring Boot CI/CD pipeline!", response);
    }
}
