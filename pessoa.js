import mongoose from "mongoose";

const PessoaSchema = new mongoose.Schema({
    name: String,
    email: String
})

export default mongoose.model("Pessoa",PessoaSchema);