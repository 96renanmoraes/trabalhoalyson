
// Função para capturar e consultar os dados do cliente via GET
async function buscaCliente(){
    // Obtém o CPF inserido no campo de input
    const consunta_cpf = document.getElementById('cpf').value; 
    
    // Verifica se o CPF foi informado
    if (!consunta_cpf){
        alert('Por favor, insira um CPF');
        return;  // Interrompe a execução caso o CPF não tenha sido informado
    }
    
    try {
        // Faz a requisição para consultar os dados do cliente
        const response = await fetch(`http://127.0.0.1:5000/buscaCliente?doc=${consunta_cpf}`)
        
        // Verifica se a resposta da API foi bem-sucedida
        if (response.ok){
            const dados = await response.json();
            console.log(dados)
            //document.getElementById('saída').textContent = json.stringify(dados)
            
            // Verifica se o cliente foi encontrado
            if (dados.nome === "não encontrado") {
                alert('Cliente não encontrado!');
            } else {
                // Exibe os dados do cliente na tela
                document.getElementById('nome_saida').textContent = dados.nome;
                document.getElementById('nasc').textContent = dados.data_nascimento;
                document.getElementById('email').textContent = dados.email ;
            }
        } else {
            alert('Erro ao consultar cliente');
        }
    } catch (error) {
        alert('Erro de conexão com o servidor');
    }
}

// Função para capturar os dados do novo cliente e fazer a requisição POST
async function salvar_cliente(){
    // Captura os dados do novo cliente a partir dos campos do formulário
    const nome = document.getElementById('nome_cliente').value;
    const dataNascimento = document.getElementById('data_nascimento').value;
    const email = document.getElementById('email_cliente').value;
    const cpf = document.getElementById('cpf_cliente').value;

    // Verifica se todos os campos foram preenchidos
    if (!nome || !dataNascimento || !email || !cpf) {
        alert('Por favor, preencha todos os campos!');
        return;
    }

    try {
        // Envia os dados para o backend usando uma requisição POST
        const response = await fetch('http://127.0.0.1:5000/salvar_cliente', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            
            body: JSON.stringify({
                nome: nome,
                data_nascimento: dataNascimento,
                email: email,
                cpf: cpf
            })
        });

        // Verifica a resposta do backend
        if (response.ok) {
            const dados = await response.json();
            if (dados.message === "CPF já existe") {
                alert('Erro: CPF já cadastrado!');
            } else {
                alert('Cliente salvo com sucesso!');
            }
        } else {
            alert('Cliente salvo com sucesso!');
        }
    } catch (error) {
        alert('Erro de conexão com o servidor');
    }
}