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
var getResponse = async() =>{
    await manager.train();
    manager.save();
    const response = await manager.process('en', 'bye bye take care');
    console.log(response.answer);
    return response;
}
getResponse();



