# -*- coding: utf-8 -*-
"""Simple fact sample app."""

import random
import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response


# =========================================================================================================================================
# GLOBALS
# =========================================================================================================================================
SKILL_NAME = "Cosmica"
GET_FACT_MESSAGE = "Here's your fact: "
HELP_MESSAGE = "You can say tell me a space fact, or, you can say exit... What can I help you with?"
HELP_REPROMPT = "What can I help you with?"
STOP_MESSAGE = "Goodbye!"
FALLBACK_MESSAGE = "The Space Facts skill can't help you with that.  It can help you discover facts about space if you say tell me a space fact. What can I help you with?"
FALLBACK_REPROMPT = 'What can I help you with?'
EXCEPTION_MESSAGE = "Sorry. I cannot help you with that."

SCENARIO_NAME = 0
DIALOG = 1
CHOICE1 = 2
CHOICE2 = 3
EXIT = 4
CREW_MORALE = 5
SHIP_STRENGTH = 6
INTEL = 7

# =========================================================================================================================================
# Scenario Data
# =========================================================================================================================================

scenarios = [] # scenario data
scenarios_seen = [] # keep track of scenarios that have been seen so far


scenarios.append({SCENARIO_NAME:'put name of scenario here',
                  DIALOG:'put dialog here',
                  CHOICE1:'choice should be YES-1 or NO-2, etc where the 1 and 2 are the array ID of next scenario to go to',
                  CHOICE2:'other possible choice',
                  EXIT:'type EXIT here if this dialog then ends the scenario starting a new one',
                  CREW_MORALE:'place a positive or negative integer if crew morale is affected by this outcome',
                  SHIP_STRENGTH:'place a positive or negative integer if ship strength is affected by this outcome',
                  INTEL:'place a positive or negative integer if intel is affected by this outcome'})

# temp load of scenario for testing
scenarios.append({SCENARIO_NAME:'DISTRESS CALL 1',
                  DIALOG:'Captain, I have picked up a distress call coming from the vega system, would you like for us to respond?',
                  CHOICE1:'YES-3',
                  CHOICE2:'NO-2',
                  EXIT:'',
                  CREW_MORALE:'',
                  SHIP_STRENGTH:'',
                  INTEL:''})
scenarios.append({SCENARIO_NAME:'DISTRESS CALL 1',
                  DIALOG:'Aye Aye Captain, we will avoid this beacon. Spock Says, Good thinking Captain, after further analysis, I believe this signal shows a similar pattern to onse that the USS Cole fell victom to as an Alrick Von Monicko decoy. We might have gained some interesting intel though.',
                  CHOICE1:'',
                  CHOICE2:'',
                  EXIT:'EXIT',
                  CREW_MORALE:'',
                  SHIP_STRENGTH:'',
                  INTEL:'5'})
scenarios.append({SCENARIO_NAME:'DISTRESS CALL 1',
                  DIALOG:'Captain, we are arriving at the coordinates of the distress call. Ohura calls out, Captain we are reading multiple distress calls from a vulcan cruiser, Spock Says, Captain, scans show multiple life forms on the ship, however their signals are weaker than expected. Shall we send a boarding crew to investigate?',
                  CHOICE1:'YES-4',
                  CHOICE2:'NO-2',
                  EXIT:'',
                  CREW_MORALE:'',
                  SHIP_STRENGTH:'',
                  INTEL:''})
scenarios.append({SCENARIO_NAME:'DISTRESS CALL 1',
                  DIALOG:'You beam on board the Cruiser and notice a strange acidic smell that burns your nostrils. After placing breathing masks Seargent Oleg calls out, Captain! Over here! I am detecting multiple strange life signals from the room ahead. Scotty also calls out, Captain! I am detecting a strange power surge from what looks like the engine room, this could be trouble, the hyper drive could be going critical soon. Say Engine Room or Life forms to direct your crews next action.',
                  CHOICE1:'ENGINE ROOM-5',
                  CHOICE2:'LIFE FORMS-6',
                  EXIT:'',
                  CREW_MORALE:'',
                  SHIP_STRENGTH:'',
                  INTEL:''})
scenarios.append({SCENARIO_NAME:'DISTRESS CALL 1',
                  DIALOG:'Scotty says, Captain, it looks like the hyper drive is in critical condition and unstable, at most we have minutes before the drive blows. If I focus on this, we will not have enough time to deal with the survivors, do you want us to stay or resecue the survivors? Say Stay or Rescue to direct your crews next action.',
                  CHOICE1:'STAY-8',
                  CHOICE2:'RESCUE-6',
                  EXIT:'',
                  CREW_MORALE:'',
                  SHIP_STRENGTH:'',
                  INTEL:''})
scenarios.append({SCENARIO_NAME:'DISTRESS CALL 1',
                  DIALOG:'You manage to access the room and your crew discoveres a handful of vulcan aliens tending to their wounded.  Scotty calls out, Captain! I am detecting a dangerous increase in hyperdrive levels from the engine room, we need to beam off this ship! Do you bring the wounded vulcan aliens with your crew?',
                  CHOICE1:'YES-7',
                  CHOICE2:'NO-8',
                  EXIT:'',
                  CREW_MORALE:'',
                  SHIP_STRENGTH:'',
                  INTEL:''})
scenarios.append({SCENARIO_NAME:'DISTRESS CALL 1',
                  DIALOG:'The Cruiser explodes at a safe distance and after some time in the medical bay Ohura declares, Captain, we managed to piece together what happened, it is a good thing we saved this crew, we learned some valueable information about Von Monikos pirate fleet from some of the discussions and readings they brought with them as we were leaving the ship.',
                  CHOICE1:'',
                  CHOICE2:'',
                  EXIT:'EXIT',
                  CREW_MORALE:'',
                  SHIP_STRENGTH:'',
                  INTEL:'10'})
scenarios.append({SCENARIO_NAME:'DISTRESS CALL 1',
                  DIALOG:'The Cruiser explodes at a safe distance and after some time the Scotty says, Captain, we managed to gather some interesting technology which we think will help increase our ships strength, however, the crew is not happy that we abandoned a crew in need.',
                  CHOICE1:'',
                  CHOICE2:'',
                  EXIT:'EXIT',
                  CREW_MORALE:'-10',
                  SHIP_STRENGTH:'10',
                  INTEL:''})


data = [
  'A year on Mercury is just 88 days long.',
  'Despite being farther from the Sun, Venus experiences higher temperatures than Mercury.',
  'Venus rotates counter-clockwise, possibly because of a collision in the past with an asteroid.',
  'On Mars, the Sun appears about half the size as it does on Earth.',
  'Earth is the only planet not named after a god.',
  'Jupiter has the shortest day of all the planets.',
  'The Milky Way galaxy will collide with the Andromeda Galaxy in about 5 billion years.',
  'The Sun contains 99.86% of the mass in the Solar System.',
  'The Sun is an almost perfect sphere.',
  'A total solar eclipse can happen once every 1 to 2 years. This makes them a rare event.',
  'Saturn radiates two and a half times more energy into space than it receives from the sun.',
  'The temperature inside the Sun can reach 15 million degrees Celsius.',
  'The Moon is moving approximately 3.8 cm away from our planet every year.',
]

# =========================================================================================================================================
# Editing anything below this line might break your skill.
# =========================================================================================================================================

sb = SkillBuilder()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# Built-in Intent Handlers
class GetNewFactHandler(AbstractRequestHandler):
    """Handler for Skill Launch and GetNewFact Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_request_type("LaunchRequest")(handler_input) or
                is_intent_name("GetNewFactIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In GetNewFactHandler")

        random_fact = random.choice(data)
        speech = GET_FACT_MESSAGE + random_fact

        handler_input.response_builder.speak(speech).set_card(
            SimpleCard(SKILL_NAME, random_fact))
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In HelpIntentHandler")

        handler_input.response_builder.speak(HELP_MESSAGE).ask(
            HELP_REPROMPT).set_card(SimpleCard(
                SKILL_NAME, HELP_MESSAGE))
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In CancelOrStopIntentHandler")

        handler_input.response_builder.speak(STOP_MESSAGE)
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for Fallback Intent.

    AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")

        handler_input.response_builder.speak(FALLBACK_MESSAGE).ask(
            FALLBACK_REPROMPT)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")

        logger.info("Session ended reason: {}".format(
            handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response


# Exception Handler
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.info("In CatchAllExceptionHandler")
        logger.error(exception, exc_info=True)

        handler_input.response_builder.speak(EXCEPTION_MESSAGE).ask(
            HELP_REPROMPT)

        return handler_input.response_builder.response


# Request and Response loggers
class RequestLogger(AbstractRequestInterceptor):
    """Log the alexa requests."""
    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.debug("Alexa Request: {}".format(
            handler_input.request_envelope.request))


class ResponseLogger(AbstractResponseInterceptor):
    """Log the alexa responses."""
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.debug("Alexa Response: {}".format(response))


# Register intent handlers
sb.add_request_handler(GetNewFactHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# Register exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

# TODO: Uncomment the following lines of code for request, response logs.
sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger())

# Handler name that is used on AWS lambda
lambda_handler = sb.lambda_handler()
