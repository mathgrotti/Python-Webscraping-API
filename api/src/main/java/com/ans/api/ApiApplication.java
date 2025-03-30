package com.ans.api;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.*;
import jakarta.persistence.*;
import org.springframework.beans.factory.annotation.Autowired;
import java.util.List;

@SpringBootApplication
@RestController
@RequestMapping("/api")
public class ApiApplication {

    public static void main(String[] args) {
        SpringApplication.run(ApiApplication.class, args);
    }

    // --- Configuração JPA direta na mesma classe ---

    @Entity
    @Table(name = "operadoras")
    public static class Operadora {
        @Id
        @Column(name = "registro_ans")
        private String registroAns;

        @Column(name = "cnpj")
        private String cnpj;

        @Column(name = "razao_social")
        private String razaoSocial;

        @Column(name = "nome_fantasia")
        private String nomeFantasia;

        // Getters e Setters (OBRIGATÓRIOS)
        public String getRegistroAns() { return registroAns; }
        public void setRegistroAns(String registroAns) { this.registroAns = registroAns; }
        
        public String getCnpj() { return cnpj; }
        public void setCnpj(String cnpj) { this.cnpj = cnpj; }
        
        public String getRazaoSocial() { return razaoSocial; }
        public void setRazaoSocial(String razaoSocial) { this.razaoSocial = razaoSocial; }
        
        public String getNomeFantasia() { return nomeFantasia; }
        public void setNomeFantasia(String nomeFantasia) { this.nomeFantasia = nomeFantasia; }
    }

    // Correção: Usar EntityManager através do Spring
    @Autowired
    private EntityManager entityManager;

    @GetMapping("/operadoras")
    public List<Operadora> getOperadoras() {
        // Correção: JPQL deve referenciar o nome da classe de entidade
        return entityManager.createQuery("SELECT o FROM Operadora o", Operadora.class)
                          .getResultList();
    }

    @PostMapping("/operadoras")
    public Operadora createOperadora(@RequestBody Operadora operadora) {
        // Correção: Transação necessária para operações de escrita
        entityManager.getTransaction().begin();
        entityManager.persist(operadora);
        entityManager.getTransaction().commit();
        return operadora;
    }
}