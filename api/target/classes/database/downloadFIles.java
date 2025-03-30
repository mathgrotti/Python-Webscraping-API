import java.io.FileOutputStream;
import java.io.IOException;
import java.net.URL;
import java.nio.channels.Channels;
import java.nio.channels.ReadableByteChannel;

public class DownloadFiles {
    public static void main(String[] args) {
        // URLs dos arquivos
        String[] financialUrls = {
            "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2022/",
            "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2023/"
        };
        String operatorsUrl = "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/Operadoras_ativas.csv";
        
        try {
            // Download dos arquivos financeiros
            for (String baseUrl : financialUrls) {
                // Aqui você precisaria listar os arquivos no diretório e baixar cada um
                // Implementação simplificada para demonstração
                String fileUrl = baseUrl + "Demonstrações_Contábeis.zip"; // exemplo
                downloadFile(fileUrl, "data/financial_" + baseUrl.substring(baseUrl.length() - 5, baseUrl.length() - 1) + ".zip");
            }
            
            // Download do arquivo de operadoras
            downloadFile(operatorsUrl, "data/Operadoras_ativas.csv");
            
            System.out.println("Downloads concluídos com sucesso!");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    
    private static void downloadFile(String urlStr, String outputFile) throws IOException {
        URL url = new URL(urlStr);
        ReadableByteChannel rbc = Channels.newChannel(url.openStream());
        FileOutputStream fos = new FileOutputStream(outputFile);
        fos.getChannel().transferFrom(rbc, 0, Long.MAX_VALUE);
        fos.close();
        rbc.close();
    }
}