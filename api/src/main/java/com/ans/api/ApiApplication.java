package com.ans.api;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.*;
import org.springframework.beans.factory.annotation.Autowired;
import javax.sql.DataSource;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;

@SpringBootApplication
@RestController
@RequestMapping("/api")
public class ApiApplication {
    
    @Autowired
    private DataSource dataSource;

    public static void main(String[] args) {
        try {
            SpringApplication.run(ApiApplication.class, args);
        } catch (Exception e) {
            System.err.println("Falha na inicialização:");
            e.printStackTrace();
        }
    }

    @GetMapping("/operadoras")
    public List<Operadora> searchOperadoras(@RequestParam String searchTerm) {
        List<Operadora> results = new ArrayList<>();
        
        try (Connection conn = dataSource.getConnection()) {
            String sql = "SELECT * FROM operadoras WHERE razao_social LIKE ? OR nome_fantasia LIKE ? LIMIT 10";
            PreparedStatement stmt = conn.prepareStatement(sql);
            stmt.setString(1, "%" + searchTerm + "%");
            stmt.setString(2, "%" + searchTerm + "%");
            
            ResultSet rs = stmt.executeQuery();
            while (rs.next()) {
                Operadora op = new Operadora();
                op.setRegistroAns(rs.getString("registro_ans"));
                op.setRazaoSocial(rs.getString("razao_social"));
                op.setNomeFantasia(rs.getString("nome_fantasia"));
                // set outros campos...
                results.add(op);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        
        return results;
    }
}

class Operadora {
    private String registroAns;
    private String razaoSocial;
    private String nomeFantasia;
    // outros campos...
    
    // getters e setters
    public String getRegistroAns() { return registroAns; }
    public void setRegistroAns(String registroAns) { this.registroAns = registroAns; }
    public String getRazaoSocial() { return razaoSocial; }
    public void setRazaoSocial(String razaoSocial) { this.razaoSocial = razaoSocial; }
    public String getNomeFantasia() { return nomeFantasia; }
    public void setNomeFantasia(String nomeFantasia) { this.nomeFantasia = nomeFantasia; }
    // outros getters e setters...
}