import openai
import os
from dotenv import load_dotenv
import openai

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

openai.api_type = "azure"
openai.api_base = endpoint 
openai.api_version = "2024-05-01-preview"  # Adjust the version based on your Azure resource setup
openai.api_key = api_key 

def judge_submission(submission):
    prompt = """
    I would like you to evaluate an AI-based prototype idea using five key criteria: 
    1. Impact (10 points)
    2. Feasibility (10 points)
    3. Implementation & Scaling (10 points)
    4. Team Capabilities (10 points)
    5. Technical Sophistication (10 points)
    6. Use of AI & ML Technologies (5 points)
    7. Use of Available Data (5 points)
    8. Interface Design Plans/Consumability (5 points)
    For each criterion, I need scores from 1 to 10 or 1 to 5 (The higher number, the better, 65 points in total), along with a brief explanation of why the score was given.
    
    Example 1:
    Submission: {
    Problem Description: To properly cement the foundations of the issue that drives our entire endeavor, we must first confront a raging epidemic of community-based discrimination around the internet that unintentionally targets the visually impaired. As of this very moment, around 59.5 percent of the global population have access to the internet; and there are over 43 million people in the world that are diagnosed as clinically blind, with an additional, awe-striking 295 million people living with various degrees of visual impairment. With such an astronomical number of people around the globe suffering from serious visual impairment every day, less than 1 percent of the 1.7 billion websites around the internet actually offer any sort of accessibility-accommodation.
    With practically all of websites still “barring” the visually impaired from browsing their contents and accessing their resources, an inherent discrimination against the visually impaired has emerged. For instance, if George, a hypothetical individual, whose visual impairment is very much real and shared by many, wants to buy a sweater from the H&M website or to browse some antiques on Ebay, he probably would not even be able to begin without the assistance of a  visually-enabled individual since he simply can not see what is on the webpage. 
    We aim to solve this issue by using AI-based software to translate these normally visual-based descriptors and overall descriptions into verbal pronunciations. Admittedly, we acknowledge the fact that there are, undoubtedly, a series of technological challenges that this project currently faces with the available technologies. For instance, for the successful fulfillment of our collective vision, we will need a robust set of AI-based image-recognition system.
    Nonetheless, we are confident in our collective abilities to realize our vision, and we are eager to confront and overcome any challenges that may face us along the way.
    Proposed Solution Description: In terms of bringing forth a comprehensive solution to our problem, we begin the design process by focalizing on the intuitive user-experience of our product. We will be delivering the finished software in the form of a google-chrome-extension that will essentially serve as a verbal-translator of the content of which the web pages that a visually-impaired individual is browsing. 
    For instance, the grocery homepage on Walmart.com would display a series of different vegetables and other produce, a easy enough set of selection for a regular person, but complex enough to cause serious difficulties for the visually-impaired. By enabling our chrome-extension, the contents, particularly the products, on the webpage will be recognized by the AI, and verbalized via speech-generation software. In other words, the grocery homepage will be pronounced out-loud to the individual in vivid, but nonetheless simple and streamlined, description. Finally, we plan on developing an “assistant-checkout” option, where the extension will assist with entering the payment information, and assist with the checkout and shipping-registration process.
    Additionally, We plan on building in a variety of customizable options for the chrome-extension. For instance, there will be a "color-enabled" option where the colors of the product will be pronounced out-loud for the visually impaired, particularly those who were not born blind and have extensive knowledge on the various shades of color. Another toggle that we are currently considering is the "description-length" toggle, where the user can customize the projected length and amount of detail-elaboration that is incorporated and pronounced for each product displayed.
    We welcome the simplicity of the entire user experience of our software, and we recognize the unique nature of this specific, combination of AI-based technologies, a combination that we hope will be able to democratize a large portion of the internet for millions of users.
    Team Description&Capability: Currently, our team is comprised of a group of extremely gifted individuals, with a wide array of skill sets, and originate from a diverse set of personal and academic background. For instance, we currently have two committed team members, who are majoring in Computer Science, with one having done extensive research on the topic of AI development, both for academic, as well as personal, interests; and the other having had experiences in the past of personally coding and building an AI "bot" from the ground-up. We also have committed members from various other majors, such as HCDD( Human design), aerospace engineering, as well as chemistry, all with various extent of exposure to coding and AI development. 
    In terms of team management and interpersonal communication, the team has committed itself from day-one to cultivate an atmosphere of equal distribution of opportunity and responsibility, of open-mindedness and judgment-free thinking, and of respect and friendship-building. In fact, our collectively elected "team leader" should really be considered as more of a team liaison, where he is in charge of the distribution of communiques and the management of time-effectiveness; rather than "boss-ing" people around. 
    Lastly, we have compiled a list of currently-committed members with their self-nominated, most noteworthy skills:
    Andy: python; java; javascript; HTML
    John: project management; interpersonal communications; public relations
    Minseo: java; UI/UX design
    Louie: Team Liaison
    Pranay: website-building experience; analyzing data; machine learning; python; R
    Kaile: python java; C; research on AI
    Special Technical Advisor: Philip Voorhees, ATAC (Penn State IT, Office of the Deputy CIO: Manager of the IT Accessibility Team)
    Use of AI Technology: The software of which we are looking to develop incorporates a variety of different AI-empowered operations. For instance, the very first step of operation for the completed Chrome-extension will be a combination of object and text recognition, where the AI will scan the webpage, recognizing the objects, or products, that are depicted on the page, as well as the text-based elements for the products, such as its price and available inventory. 
    Then, the AI-based software will work to generate and compile a list of essential elements from the object-recognition portion of the Chrome-extension, such as the products' colors, shapes, and sizes, etc...
    With all of the essential descriptors, or critical pieces of descriptive elements, collected and compiled, the software will proceed to prioritize the information based on a predetermined AI algorithm. For instance, a watermelon on the grocery shopping page of Walmart.com will generate descriptors such as green, round, relatively big, selling for $5.99 per melon, and being a watermelon. with those elements collected, the AI will recognize that the most important piece of information is that the produce is a watermelon; then it is import that the watermelon is selling for $5.99 per melon; after that, it is important that it is of the green variety, not the yellow one; finally, it is, perhaps, the least important that the watermelon is relatively big. 
    With the prioritized list of descriptors compiled, the AI will proceed to pronounce and verbalize the details using AI-based text to speech systems, image-recognition systems, computer vision systems, speech generation, and potentially others, delivering the information to our visually-impaired users.
    }
    Evaluation:
        1. Impact: 6.41; The only benefit to using this over screen readers seems to be to fill in the alt text on images and to deplace the color names. Seems like a nice idea that could have real impact on the blind community. Problem seems hard but tractable and the prototype is a nice start.  Documentation shows that they have a hold on the basic technical requirements.
        2. Feasibility: 6.94
        3. Implementation & Scaling: 6.94 
        4. Team Capabilitis: 6.53
        5. Technical Sophistication: 6.82
        6. Use of AI & ML Technologies: 3.47; Can this application be launched and used with SIRI/Alexa or other existing tools? 
        7. Use of Available Data: 3.29
        8. Interface Design Plans/Consumability: 3.35
        9. Total Score: 43.76
    
    Now, evaluate the submission: {submission} give the score as shown in the example. Summarize the project in three sentences.
    
    """

    response = openai.ChatCompletion.create(
        deployment_id="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI judge."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=800,
        temperature = 0,
        top_p = 0.9
    )

    return response['choices'][0]['message']['content']

# Example submission
submission = {"Problem Description": "Loc, our team visionary, and Ho Chi Minh City native, was fortunate to be raised by a supportive family and enjoy an advanced healthcare system. During the summers, Loc stayed in Vinh Long, a rural area located 93 miles away from the city, to visit his relatives. However, one summer, when Loc returned, his life changed. He witnessed his uncle describing hallucinations of deceased relatives and being auditorily disturbed at night. What he witnessed were symptoms of schizophrenia. Despite the severity of his uncle’s disorder, Loc’s family was unaware of its consequences. Upon taking Loc’s uncle to the local hospital he was dismissed. Lacking psychiatric knowledge, the local medical professional incorrectly explained that his symptoms were the consequence of overwork, and they suggested getting more sleep. Two months later, his uncle’s untreated symptoms worsened, and he had to travel 93 miles away to reach the nearest psychiatrist. He was then diagnosed with schizophrenia but due to delayed intervention, his disorder currently persists. Loc explained to us that people living in rural areas do not have many options regarding mental health care: as of 2004, there are only a few hundred psychiatrists in the entire country, which means that there are 0.06 psychiatrists per every bed in a mental health facility (Gaines, 14). Since 2004, this number has only worsened. Separated by geography, people in rural areas pay high fees to travel to the nearest state hospitals. In parallel with many other cultures, Vietnamese people tend not to consider mental disorders seriously. People typically seek cheaper traditional medicine, which is not scientifically credible, and going to see a psychiatrist is a last-resort option (Gaines, 13). Limited numbers of medical professionals, geographic struggles, and traditional beliefs all harmfully compromise the treatment outcome of ongoing psychotic individuals.",
              "Proposed Solution Description" : "To many countries including Vietnam, the lack of accessible mental health services is a persistent threat to global health. The SchizophrenAI brand aims to be a mental health resource that promotes awareness and accessibility within these areas through the pairing of AI technology, an online platform, and integrated humanitarian aid. Our online platform will be designed to reach users who live in areas with inadequate access to clinical psychiatrists. Patients in these areas concerned with their mental health will typically interact with the local medical professionals as their first course of action. Currently, these medical professionals are untrained at recognizing the signs of mental disorders, and incorrectly send their patients home with no further assistance. On average, nearly 90% of individuals requiring treatment for schizophrenia in low-income countries do not receive treatment (Wainberg). Instead, SchizophrenAI aims to create a platform that will provide the local medical professionals with improved objective tests to prevent them from missing a diagnosis. These objective tests, proven through psychiatric research studies and clinical practices, can increase recommendation accuracy(SITED). Through AI, we will extract the most important indicators of schizophrenia and feed these features into our algorithm. Our AI technology and algorithms can work because they will be trained on several datasets created in academic research and on data that our team aims to produce. While both types of these datasets are limited due to health privacy concerns, we plan to utilize transfer learning which can apply large, generic datasets to our specific needs, negating this issue. Beyond being a tool, the SchizophrenAI brand aims to spread mental health awareness, reduce its stigma, and to connect people in need with the resources they deserve.",
              "Team Description & Capability" : "Our team is very capable of executing the proposed idea. Our team covers each of the skill sets necessary to produce our project including multiple fullstack web and application developers. We also have multiple people with research experience applying artificial intelligence, and subject matter experts in biochemistry, business development, and UX design. First, our visionary Loc has a passion for our product, and is personally invested due to his uncle with schizophrenia, who at one point struggled to access the medical help and diagnosis he needed. Our application lead Frederick Sion is a backend developer at startup WeAreLiving and has experience with application frameworks and cloud technologies such as Firebase and Node.js. Also on the team is John Keeling, a full stack developer with experience working at FreddieMac. Maria Czura has been a UX designer for Shopala, and has talent for creating high fidelity prototypes. In regards to entrepreneurship, Gia Nguyen was a MIT LaunchX competition finalist, and continues to use her skills as business representative for EDG in Texas. Within our AI team, computer vision expert Samarth Tehri, has applied his vast knowledge of AI doing research modeling driver behavior. Also on our AI team, machine learning researcher Parker Sell aims to apply his experience in NLP towards our project. Additionally, due to his previous project management experience leading the club “DevPSU Startup,” Parker is a driving management force within the team. The final piece of our AI team, Thomas Foltz is currently focused on emotion perception AI technologies within his research. We also have biochemistry major Shawn Hu as subject matter expert, who has advanced experience doing cancer research. Our other consultants, Carlton, accounting major, and Keith, neuroscience major, are providing our team with extra expertise to ensure competence and quality.",
              "Use of AI Technology" : "The SchizophrenAI team plans to utilize three methods of extracting mental health recommendations using artificial intelligence. The first objective way of recognizing schizophrenia uses generalized facial expressions. In a research work named SchiNet a convolutional neural network (CNN) is used to further analyze patient interviews(Bishay). By using CNN’s to crop the videos so that just the patient remains, the network outputs the predicted symptoms (such as flat affect, poor rapport, lack of spontaneity, etc…) as classified in the Positive and Negative Syndrome Scale. Trained psychiatrists commonly utilize this scale to determine whether or not a person should be diagnosed with Schizophrenia. By classifying the patient’s facial and bodily expressions according to this scale, we can better assist a medical professional in understanding the patient. Secondly, computer vision will be used to interpret minute eye movements. Several papers indicate a correlation between irregular eye movements and schizophrenia during objective tests(Sears). Typically, to recognize these irregularities, the video must be manually annotated to pinpoint the exact milli-second delay present in schizophrenic patients. Computer vision tools like a CNN will be able to more accurately calculate this. Finally, our solution utilizes natural language processing to analyze a patient’s speech. The patient's recorded response is translated to text with the best possible text-to-speech system. Next, the translated text will be analyzed using a neural network proposed by Harvard researchers(Rezaii). Specifically, this network determines the semantic density of the patient’s speech, or the level of the meaning in a patient’s words. Since low density levels are correlated with psychosis, a major symptom of schizophrenia, this will provide key insights about the patient(Rezaii). Facial expression analysis, eye movement delay calculation, and language analysis combined can provide a more objective test."
              }
score = judge_submission(submission)

with open("Innovation-Engine\Prototype-Judge\judge_output.txt", "w") as file:
    file.write(score)

print("Output saved to judge_output.txt")