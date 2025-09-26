import mongoose from "mongoose";

const UsuarioSchema = new mongoose.Schema({
    name: String,
    email: String
})

export default mongoose.model("usuario",UsuarioSchema);