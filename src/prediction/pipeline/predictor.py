from prediction import logger
from prediction.config.configuration import ConfigManager
import mlflow
from ensure import ensure_annotations

class Predictor:
    def __init__(self, config_manager: ConfigManager) -> None:
        self.config_manager = config_manager

    @ensure_annotations
    def predict(self, text: str) -> list:
        pyfunc_loaded = mlflow.pyfunc.load_model(self.config_manager.config.mlflow.model_uri)
        logger.info(f'Predicting with mode {self.config_manager.config.mlflow.model_uri} for text: \n{text}')
        # inference_config will be applied
        result = pyfunc_loaded.predict(text)
        return result
    
if __name__ == '__main__':
    cm = ConfigManager()
    predictor = Predictor(cm)

    text = """
    Spasimir Dinev: Your age, so space. Can you go to the to the first slide most def?
Spasimir Dinev: All right, so first, we're a few months, OK? We're not machines. So, so quite often people expect that they come to us. They use the question and we immediately bring the answer. That's not help, right? The search is a craft and it it requires its time.
Spasimir Dinev: How long answering your research question will take the doesn't depend on how long the question is right? It depends of how deep you need to dig. We have our tools, but they have their limits, so keep in mind that we cannot really discover everything, although we can do quite hard. So that's the first thing we're humans with shovels. So can we look at the next one?
Spasimir Dinev: Although we see the future.
Spasimir Dinev: It is science. It's not magic. OK, so as as a social science research is a social science, it has its, you know, rules in ways things are get done. So please, when you work with the researcher.
Spasimir Dinev: Take notes of the things that they ask in terms of methodology and why things should be done. Believe me, we can manipulate the answers, we can get the right answers. The dancers you want to hear. But we've been asked. Yeah, but that's not what we what we try to science, social science so and go to the next one.
Spasimir Dinev: Especially now that we have like expanding into different markets, I mean how how we study conversation, it's on your lecture. So let's keep it was very important.
Spasimir Dinev: Uh in the whole company, we are missing marketing researchers. OK, that's this animal we're really missing because the insights team crunches internal data. You access your focus on the experience, but we like market research data. Up to recently, we actually been purchasing and all these entering exact moment.
Spasimir Dinev: Because for us, you knowing.
Spasimir Dinev: Umm, so uh, I hope that and funny I hope. I hope that soon we're gonna have couple marketing researchers that can help us with competitive because someone needs to monitor specific markets constant, what are their launching, what is their value proposition, what is their pricing and so on and so forth. Currently from time to time we help with this basically we do test script search that's the easiest way you start right. And then of course through user testing we are getting users of those products and actually exploring we have them.
Spasimir Dinev: Fantastic exploration on on them on them. Why then rocks in the US, we can send you the presentation only Toro, for example, earlier doctors of the Toro, were they like how etoro tracks and so on. So we can do that. But we we kind of try to stick with.
Spasimir Dinev: With the current, this is something that we hope, uh, external support would be. So let me have that. We have the new strategy perform, so that would be the one after six months and be able to help a little more with overarching competitive research. But it also needs to be product responsibility too. So like for your specific area that you're working on, you should be aware of what the competitors would building and how do we differentiate.
Spasimir Dinev: So that we have a great example with Nigeria last year where we the AML team was seeing massive volumes of flows through the crypto exchanges and we didn't have our crypto product active in Nigeria. We just said well, why, why didn't someone else see our lunch and we switched on. You switch on crypto and you know some money, right? So again it's something we all see right in our data jobs. You see the flows, we see what's going on, we see what the competitors are doing. We see it even that users, right.
Spasimir Dinev: Yeah, that'd be great. That for jobs, yeah.
Spasimir Dinev: Ohh for sure. Something each of the be interest. Start doing your board right. Remember that start by adding your knowledge and you will see that in in one month you're gonna have quite good picture of what is happening in your. In your specific you want.
Spasimir Dinev: I'm just on the computer.
Spasimir Dinev: So it's there is an outlook aspect to it because you can't know everything about everyone, everywhere. It's obviously like a lot of time to really dive deep into into anything, but when you have a kind of from your own expertise and for designers, we don't just go around and say what can we take all of this is I'm gonna transfer it to my what I did some amazing. But what what we're seeing is if I have how my tweet and I have some solutions based and if some solution that somebody came up with loosely answers the question and helps me.
Spasimir Dinev: Well, you know I'm I can use it then. So basically I'll do competitive analysis over question, how can I?
Spasimir Dinev: So for like for the people thing right, we don't need to have all of the original ideas. It's all the original to have Twitter and somebody already did it. But it's kind of if you understand your kind of what competition does in your specific case, you can help yourself achieve last weekend.
Spasimir Dinev: Just one more thing about the competitive research I used to please the because the pending on the areas and areas we haven't found that the funding more and have solved with.
Spasimir Dinev: Then are they a lot of region? Yeah, all kind of this. I mean Google.
Spasimir Dinev: It's just it takes time and in current chips.
Spasimir Dinev: That's the goal we should. I had so many jokes in there.
Spasimir Dinev 57 minutes
So poor.
Spasimir Dinev: It's going. It's so I'll keep it for tomorrow.
Spasimir Dinev: It's only interesting.
Spasimir Dinev: It was difficult.
Spasimir Dinev: A researcher PM in the designer and there's a bar.
Spasimir Dinev: OK, OK.
    """

    prediction = predictor.predict(text)
    print(f'Prediction: {prediction}')