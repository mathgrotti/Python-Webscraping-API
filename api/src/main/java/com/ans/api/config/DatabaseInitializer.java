package com.ans.api.config;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.ClassPathResource;
import org.springframework.jdbc.datasource.init.ScriptUtils;
import org.springframework.stereotype.Component;

import javax.annotation.PostConstruct;
import javax.sql.DataSource;
import java.sql.Connection;
import java.sql.SQLException;

@Component
public class DatabaseInitializer {

    @Autowired
    private DataSource dataSource;

    @PostConstruct
    public void initDatabase() {
        try (Connection connection = dataSource.getConnection()) {
            // Executa o script de setup que está em database/setup.sql
            ScriptUtils.executeSqlScript(connection, 
                new ClassPathResource("database/setup.sql"));
            
            // Opcional: Executar outros scripts como analytics.sql se necessário
            // ScriptUtils.executeSqlScript(connection,
            //     new ClassPathResource("database/analytics.sql"));
            
        } catch (SQLException e) {
            throw new RuntimeException("Falha ao inicializar banco de dados", e);
        }
    }
}