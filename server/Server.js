import express from 'express';
import Usuario from "./UsuarioSchema.js";
import connectDB from './MongoDB.js'


const server = express();
const PORT = 3000
connectDB();

server.use(express.json()) //o middleWare para tratar as informações recebidas em json.

server.get("/", async (req, res) => {
    try {
        const usuarios = await Usuario.find();
        return res.json(usuarios);
    } catch (error) {
        return res.status(500).json({ error: error });
    }
});

server.post("/", async (req, res) => {
    try {
        const novoUsuario = await Usuario.create(req.body);
        return res.status(201).json(novoUsuario); 
    } catch (error) {
        return res.status(400).json({ error: error.message }); 
    }
});

server.put("/:id", async (req, res) => {
    // req.params.id
    try {
        const usuarioAtualizado = await Usuario.findByIdAndUpdate(
            req.params.id,
            req.body,
            {new:true}
        );
        return res.status(201).json(usuarioAtualizado); 
    } catch (error) {
        return res.status(400).json({ error: error.message }); 
    }
});

server.delete("/:id", async (req, res) => {
    // req.params.id
    try {
        const usuarioDeletado = await Usuario.findByIdAndDelete(
            req.params.id,
        );
        return res.status(201).json(usuarioDeletado); 
    } catch (error) {
        return res.status(400).json({ error: error.message }); 
    }
});



server.listen(PORT, () => console.log("O servidor está rodando na porta: " + PORT));
