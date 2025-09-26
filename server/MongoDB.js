import mongoose from "mongoose";

const dbUrl = "mongodb://localhost:27017/sistemacrud"; 

async function connectDB() {
    try {
        await mongoose.connect(dbUrl, {});
        console.log('MongoDB conectado com sucesso!');
    } catch (err) {
        console.error('Erro ao conectar ao MongoDB:', err.message);
        process.exit(1); 
    }
}
export default connectDB;