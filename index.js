import express from 'express';
import mongoose from 'mongoose';
import dotenv from 'dotenv';
import Pessoa from "./pessoa.js";


dotenv.config();

const server = express();
const PORT = 3000

const connectMongo = async () => {
    try {
        await mongoose.connect(process.env.MONGO_URI);
        console.log("Conectado ao MongoDB")
    } catch (error) {
        console.log("Erro ao conectar ao MongoDB", error)
    }

}
connectMongo();

server.post("/", async (req, res) => {
    try {
        const pessoa = await Pessoa.create(req.body);
        res.json(pessoa);
    } catch (error) {
        res.json({error:error});
    }

});




server.listen(PORT, () => console.log("O servidor está rodando na porta: " + PORT));
server.use(express.json) //MiddleWare para tratar as informações recebidas.