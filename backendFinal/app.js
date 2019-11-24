// import express
const express = require('express');
const bodyParser = require('body-parser');
const { NlpManager } = require('node-nlp');
 
const manager = new NlpManager({ languages: ['en'] });
// Adds the utterances and intents for the NLP
const intent = require("./intent.json");
const answer = require("./answer.json");
for (var key in intent){
    if (intent.hasOwnProperty(key)){
        manager.addDocument('en', intent[key][0],intent[key][1])
    }
}

for (var a in answer){
    if (answer.hasOwnProperty(a)){
        manager.addAnswer('en', answer[a][0],answer[a][1]);
    }
}

// Train and save the model.
var getResponse = async(question) =>{
    await manager.train();
    manager.save();
    const response = await manager.process('en', question);
    return response.answer;
}

// register routes
// const truffleroutes = require('./blockroutes');

//create express app
const app = express()
app.use(bodyParser.json());

app.use((req,res,next) => {
    res.setHeader('Aceess-Controll-Allow_Origin','*');
    res.setHeader('Access-Control-Allow-Methods','GET, POST');
    res.setHeader('Access-Control-Allow-Headers','Content-Type, Authorization');
    next();
});

app.get('/', (req, res) => {
    var question = req.query.question
    getResponse(question).then(ans=>{
        console.log(ans);
        res
        .status(200)
        .send(answer)
        .end();
    }).catch(err=>{
        console.log(err);
    });
    console.log(answer);

});
// app.use('/call',truffleroutes);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () =>{
    console.log(`App listening on port ${PORT}`);
    console.log('Press Ctrl+C to quit.');  
})