import os
import json
import datetime
from openai import AzureOpenAI
from dotenv import load_dotenv
import re

# Load environment variables from the .env file
load_dotenv()
# api_key = os.getenv("AZURE_OPENAI_API_KEY")
# endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

# openai.api_type = "azure"
# openai.api_base = endpoint 
# openai.api_version = "2024-07-01-preview"  # Adjust the version based on your Azure resource setup
# openai.api_key = api_key 
# model = "gpt-4"
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-07-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_FOLDER = os.path.join(SCRIPT_DIR, "Project_folder")
CRITERIA_FILE = os.path.join(SCRIPT_DIR, "Judge_Brain", "criteria.txt")
EVALUATIONS_OUTPUT_FOLDER = os.path.join(SCRIPT_DIR, "Final Results", "Markdown Judge")


# Ensure the full path to "Final Results/Markdown Judge" is created
if not os.path.exists(EVALUATIONS_OUTPUT_FOLDER):
    os.makedirs(EVALUATIONS_OUTPUT_FOLDER)
    print(f"Created folder: {EVALUATIONS_OUTPUT_FOLDER}")


# Load judging criteria from a file
def load_judging_criteria():
    if os.path.exists(CRITERIA_FILE):
        with open(CRITERIA_FILE, 'r', encoding="utf-8") as f:
            return f.read()
    else:
        print("Criteria file not found.")
        return None

# Function to clean project name by removing date suffix
def clean_project_name(folder_name):
    return re.sub(r"_\d{2}-\d{2}-\d{2}$", "", folder_name)

# Function to evaluate a project submission using the OpenAI API
def evaluate_submission(submission_content, project_name, criteria):
    # Prepare the prompt
    # system_message = {
    #     "role": "system",
    #     "content": "You are an AI judge evaluating a project for the Nittany AI Challenge based on the provided criteria. Please provide a detailed score and summary for each criterion."
    # }

    # user_message = {
    #     "role": "user",
    #     "content": f"""
    #     Project Submission:
    #     {submission_content}

    #     Judging Criteria:
    #     {criteria}

    #     Please evaluate the project based on each criterion and provide a detailed summary and score (out of 10) for each one.
    #     """
    # }
    
    example_1_highest_score = '''
    {"submission": "2024Ni\\'anyAIChallengeSubmissionID:31TEAMINFORMATION 1.ProjectTeamName: KinderVerse 2.TeamMembers:ListeachteammemberincludingName,PSUEmail,Campus,andCollege(ex:JaneDoe,jxd123@psu.edu,Shenango,Engineering) SurajKumar,smk6961@psu.edu,UniversityPark,EngineeringLucasLigenza,lql5443@psu.edu,UniversityPark,EngineeringAneeshSingh,azs7281@psu.edu,UniversityPark,ISTDanielWoodford,dfw5416@psu.edu,UniversityPark,ISTAlexanderFoor,akf5643@psu.edu,UniversityPark,Engineering 3.PrimaryContact/TeamLead: SurajKumar,smk6961@psu.edu,814-232-0057PROJECTINFORMATION4.Problem/OpportunityStatementDocumentaGonshouldincludeanoverviewoftheproblemandthemethodusedtoaddressthatproblem.ThisshoulddemonstratethatyouclearlyunderstandtheproblemoropportunityyouareaddressingwithAI.Responseislimitedto300words. IntheaVermathoftheunfortunateCOVID-19pandemic,globalresearchshowsaconcerningdeclineinthereadingandcomprehensionlevelsofstudentsandchildren.Duetotheforcedstay-at-home,childrenspentanabundantamountofZmeonscreens,retainingnothingbene\ufb01cialfromit.Recognizingthisissue,wecreatedKinderVerse,aninnovaZvesoluZonuZlizingAItechnologiestoenhancethelearningexperienceforeverychild.Wehave\ufb01ne-tunedanLLMtogenerateeducaZonal,moral-basedstories,keepingchildrenengaged,whilecreaZngaposiZvelasZngimpact.InaddiZontoourstorygeneraZon,ourappincorporatesimagegeneraZontoillustratethestoriesandspeci\ufb01c,corevocabulary.Thisapproachaimstoenhancecomprehensionandcreateafunlearningenvironment.Weunderstandtheimportanceofachild-friendlyuserinterface,andthus,ourappcontainsadesignfeaturinglargebu^ons,interacZvestories,andvisuallyappealingimagery.Thisthough_uldesignensuresasimpleyetpowerfulexperienceforyoungminds,promoZngacZveparZcipaZonandexploraZon.Ourappensuresthatwedon\\'tuseanypersonalinformaZonforthechildrenandallthestoriesaregoingtobestoredlocally.Wealsounderstandthatthisappismeantforchildren,whichiswhywehaveinsZlledparentalaccesssotheparentsareabletomonitortheirchild\\'sprogressandwatchovertheiracZons.Inall,KinderVerseaimstobeareliablesubsZtutefortheaddicZvetechnologybyprovidingafun,yetmeaningfullearningexperience.  5.MVPUseCaseProvideasampleusecaseforthetool.DescribehowsomeonewillusetheMVPfuncGonalityyouintendtobuildandthebene\ufb01tsorimpacttheMVPwillprovide.Responseislimitedto300words. Sarah,amother,isconcernedabouthersonTom\\'swaninginterestinreadingandlearningduetoexcessivescreen9meduringthepost-COVIDera.ShediscoversKinderVerse,anappdesignedtoaddressthisveryissue,anddownloadsit,hopingtoreigniteTom\\'senthusiasmforlearning. UponopeningKinderVerse,SarahandTomarewelcomedbyauser-friendlyinterface,tailoredforchildrenwithlarge,colorfulbuFonsandengagingvisuals.Sarahsetsupapro\ufb01leforTom,andtheapp\\'sAI,poweredbyaspecializedLLM,generatesapersonalized,educa9onalstorybasedonTom\\'sageandinterests.Thesestoriesarenotonlycap9va9ngbutalsoimbuedwithmorallessons,ensuringawholesomelearningexperience. AsTominteractswiththestory,vibrant,AI-generatedimagesillustratethenarra9ve,enhancinghiscomprehensionandretaininghisinterest.Theapp\\'sinterac9veelementsencourageac9vepar9cipa9on,transformingpassivescreen9meintoaproduc9ve,educa9onalexperience. Bene\ufb01tsandImpact: KinderVerseo\ufb00ersatailoredlearningexperiencethatrevitalizeschildren\\'sreadinghabitsandenhancestheirunderstandingthroughvisuals9muli.Theappmakesscreen9meenriching,replacingaimlessscrollingwithmeaningful,moral-basedstories.Furthermore,KinderVerseensuresprivacyandsafety,storingcontentlocallyandprovidingparentalcontrolsformonitoringprogressandac9vity. OurvisionwithKinderVerseistocreateaglobalimpact,o\ufb00eringfamiliesatoolthatnotonlyentertainsbuteducates,fosteringaloveforlearninginchildren.Thisinnova9veapproachtoscreen9meisouranswertothechallengesfacedbyparentslikeSarah,whoseektonurturetheirchildren\\'smindsinanincreasinglydigitalworld. 6.DataAvailabilityDetailthedatasourcesleveragedwithintheprototypeaswellasthedatasourcesnecessaryifthisprojectmovedtoMVP.Ifavailable,pleasedetailthelocationandavailabilityofthedatasourcesand/ortheplanforcollectingthenecessarydata.Rememberthatwhilewecanprovidesomeassistancewithfindingdatasources,findingandgainingaccesstothosesourcesistheteam\\'sresponsibility.Responseislimitedto300words. FortheprototypeofKinderVerse,wecuratedadatasetofchildren\\'sstorieswithmoralthemes,targeZngthe3-5yearagegroup.ThisiniZaldataset,sourcedfromvariousonlinepla_orms,wasselectedbasedonspeci\ufb01ccriteriasuchasmoralcontent,genre,andvocabulary.ThisfoundaZonaldatasetplayedacrucialrolein\ufb01ne-tuningtheLlama2modelforgeneraZngage-appropriateandmorallyenrichedstories. AswetransiZontotheMVPphase,ourstrategyinvolvessigni\ufb01cantlyexpandinganddiversifyingourdataset.ApromisingresourceisthesubstanZalchildren\\'sstorydatasetreleasedbyFacebookafewyearsago.UZlizingthisandsimilardatasetswillallowustore\ufb01neandopZmizeourmodelmoree\ufb00ecZvely.OurapproachincludesdataaugmentaZontechniquestobroadentherangeanddepthofcontent,therebyenhancingthestorygeneraZoncapabilityandlinguisZcrichnessofourAImodel.Theteamiscommi^edtoongoingdatacollecZonandcuraZon,ensuringtheconZnualevoluZonandimprovementoftheAImodelsinuse.  ForimagegeneraZonintheprototype,weemployedpromptengineeringtechniques.However,movingtowardstheMVP,weaimtodevelopand\ufb01ne-tuneourownmodel,speci\ufb01callytailoredtothevocabularycomponentofKinderVerse.ThisshiVwillgiveusgreatercontrolovertheimagegeneraZonprocess,furtherminimizingthealreadynegligibleriskofinappropriatecontent..Toachievethis,weplantocompileacomprehensivedatasetofnouns,accompaniedbyhigh-quality,educaZonalimages.Thiswillsigni\ufb01cantlyimprovethevisuallearningaspectofourcorevocabularyfeature,enhancingtheoveralleducaZonalvalueoftheapp. OurdatastrategyisfocusedonmaintainingadynamicandrobustdatasetthatsupportsandgrowswithKinderVerse,ensuringthatitremainsacudng-edge,safe,ande\ufb00ecZvelearningtoolforchildren. 7.TechnologyProvideatechnicaldescripGonoftheapproachtheteamusedtoachieveitsproposedgoal,includingthewaysinwhichtheselectedAIplaVormsareusedwithintheprototypeandhowtheteamanGcipatesusingthoseandotherservicesintheMVPphase. Speci\ufb01cally,thedocumentaGonshouldincludealistofthecomponentsoftheselectedAIplaVormsthatareleveragedintheprototype,anyaddiGonalcomponentsthatmaybeleveragedinthedevelopmentoftheMVP,andaddiGonalservicesthatmaybenecessaryforconGnueddevelopment.Responseislimitedto350words. YourresponseprovidesacomprehensiveoverviewoftheKinderVerseprototypeanditsdevelopmentplans.Tore\ufb01neitfurtherwithinthe350-wordlimit,wecanstreamlinethetechnicaldescripZon,focusingonkeyAIcomponentsandplannedenhancements.Here\\'stherevisedversion: KinderVerse,anAI-driveneducaZonalpla_orm,uniquelycombinestwoadvancedAItechnologiestoenhancechildren\\'slearningexperience:theLanguageLearningModel(LLM)andtheImageGeneraZonModel. LanguageLearningModel(LLM):AtthecoreofKinderVerseistheLLM,builtuponthefoundaZonofthesophisZcatedLlama2model.ThisAIcomponentisresponsibleforgeneraZngcapZvaZng,moral-basedstoriestailoredtoeachchild\\'sageandinterests.ItintroducesprogressivelycomplexvocabularytofosterlinguisZcdevelopmentandincludesinteracZveelementswithdecisionpointstoenhancecogniZveskills. ImageGeneraZonModel:IntandemwiththeLLM,weemploytheDALLE-3modelforimagegeneraZon.ThismodelcreatesvividvisualrepresentaZonsofkeynounsandconceptswithinthestories,facilitaZngvisuallearningandaidingcomprehension.Theimagesareintegratedintoadynamicwordbank,encouragingchildrentocollectandlearnnewwords,thusbuildingtheirpersonaldicZonaries. UserInterfaceDesign:Theuserinterface,developedwithReactNaZve,isopZmizedformobileusage,featuringlarge,child-friendlybu^ons,engaginginteracZvestorytellingcomponents,andvisuallyappealinggraphics.Thisdesignensureseaseofuseforouryounglearners,makingthelearningprocessbothfunande\ufb00ecZve. PrivacyandSecurity:PrioriZzingprivacyandsecurity,KinderVersedoesnotuZlizepersonaldata.Allstoriesarestoredlocally,androbustcontent\ufb01lteringmechanismsareinplacetomaintainasafeandposiZvelearningenvironment.   FutureDevelopmentGoals: Enhancingaccessibilitybyintroducingadjustabletext-to-speechspeeds,mulZlingualsupport,andmorecomplexstorylayers.Improvingthee\ufb03ciencyandspeedofstorygeneraZonbyconZnuouslyenrichingtheLLMwithdiversedata.GraduallyincorporaZngadvancedvocabularytosupportricherlanguagedevelopment.ExploringaddiZonalAIservicestointroducenewfeaturesandfurtherenhancethepla_orm\\'scapabiliZes.Wealsowanttomakeaversionfortablets,asthoseareverypopularforchildrenandwouldprovideabigger,morestory-book-esqueexperience.TheseadvancementsaimtoelevateKinderVerse,makingitanincreasinglye\ufb00ecZve,enjoyable,andcomprehensiveeducaZonaltoolforchildrenworldwide. 8.PrototypeVideoOverviewAllteamssubmiXngaprototypeforreviewarerequiredtosubmitvideodemonstraGonsoftheirworkingprototypes.Thevideosmust: \u2022benomorethan5minutesinlength. \u2022explaintheintent,goals,andpotenGalimpactofthesoluGon. \u2022demonstratethebasic,workingfuncGonalityoftheprototype. \u2022beavailablethroughaYouTubelinkaccessibleforviewingbytheChallengereviewers. TheproducGonvalueofthevideoswillnotbefactoredintothereview,buttheymustclearlyandaccuratelyrepresenttheprototypefuncGonality.Tohelp, MediaCommonsatPennState providesfreeOneBu_onStudioopGonsthroughouttheCommonwealth. **SeeVideoProvidedintheFolder", "comments": "2. I feel the team seems to to addressing a much needed problem.  And I would have liked to understand exactly how this addresses the problem.  This seems to focus on meal planning and groceries.  But as a user, I am uncertain how exactly it helps beyond a simple web search."}
    '''

    example_2_average_score = '''
    {"submission": "2024Ni\\'anyAIChallenge SubmissionID:18 TEAMINFORMATION 1.ProjectTeamName: MealPrepPro-Team615 2.TeamMembers: ListeachteammemberincludingName,PSUEmail,Campus,andCollege (ex:JaneDoe,jxd123@psu.edu,Shenango,Engineering) BenjaminRathman,blr5545@psu.edu,StateCollege,Engineering ColeWeissercrw5753@psu.edu,StateCollege,CommunicaEons AidanHinnenkamp,arh6106@psu.edu,StateCollege,Engineering 3.PrimaryContact/TeamLead: BenjaminRathman,blr5545@psu.edu,717-875-5057 PROJECTINFORMATION 4.Problem/OpportunityStatement DocumentaGonshouldincludeanoverviewoftheproblemandthemethodusedtoaddressthatproblem. This shoulddemonstratethatyouclearlyunderstandtheproblemoropportunityyouareaddressingwithAI. Responseislimitedto300words. TheproblemthatourgroupidenE\ufb01edisobesity.Obesityisbecomingarampantproblemallacrosstheworld,with2billionpeopleintheenEreworldsu\ufb00ering.Allofourgroupmembershavefamilymembersthatsu\ufb00erorhavepassedduetoobesity.Obesityisofcoursetreatablewithahealthy lifestyleanddiet.Toaddressthisproblemwehavecreatedanappthatusingaresearchedformulacalculatesthedietaryneedsoftheuser.Then\ufb01ndsrecipesusingwebscrappingandmachinelearningto\ufb01ndpersonalizedresults.Fromtheselectedrecipestheingredientsarecompliedintoagrocerylist fortheusersconvenience. 5.MVPUseCase Provideasampleusecaseforthetool.DescribehowsomeonewillusetheMVPfuncGonalityyouintendtobuild andthebene\ufb01tsorimpacttheMVPwillprovide.Responseislimitedto300words. Someonewhousesthisappwillbestrugglingwithweightlossanddecidetostarttrea5ngitwithourapp.Once downloadingtheapptheywillbeaskedtoinputcharacteris5csaboutthemselves,theseincludeheight,weight, ac5vitylevel,andallergies.Theuserwillthenbeshowntheirmacroandmicronutrientneedsonaday-to-day basis.Foreachdayoftheweek,theychoosefromseveralrecipeop5onsthathavebeenselectedto\ufb01ttheircalculateddietaryneeds.Oncearecipehasbeenselectedforeach dayoftheweek,agrocerylistwillbe generatedandpresentedtotheuser.ABeraweekofuse,futurerecommendedrecipeswillbetailoredtotheuser\\'spreferences(thiswillbedonethroughaNeuralNetwork.)Someoneusingthisappwill\ufb01ndittobe extremelypersonalizedhavingrecommendedrecipesthattastedeliciouswhileallowingthemtoexplorenew  recipesandfoods.Theywillalso\ufb01ndthatusingtheappsavesthem5mewhenchoosingandpreppingmealswhilealsobeingacost-e\ufb00ec5vesolu5ontoweightloss. 6.DataAvailabilityDetailthedatasourcesleveragedwithintheprototypeaswellasthedatasourcesnecessaryifthisprojectmovedtoMVP.Ifavailable,pleasedetailthelocationandavailabilityofthedatasourcesand/ortheplanforcollectingthenecessarydata.Rememberthatwhilewecanprovidesomeassistancewithfindingdatasources,findingandgainingaccesstothosesourcesistheteam\\'sresponsibility.Responseislimitedto300words. To\ufb01ndourmicroandmacronutrientcalculaEonformulaweusedtheformulaprovidedbyHarvard.eduwhichtheyfoundfromextensiveresearch.Webscrapingwill\ufb01ndrecipesthat\ufb01ttheuser\\'sneedsbasedonthepreviouscalculaEons.WhilewebscrappingforcommercialusesinsomecasesisillegallawsliketheComputerFraudandAbuseAct(CFAA)intheUnitedStatesprohibitedwebscrappingifoneneedstoinputapasswordstogainaccess.Thereareseveraldatabasescontainingmanyrecipesforpublicusethatarefree,theyincludebutarenotlimitedto,PinchofYumandFood.com.Afuturegoalwouldbetopartnerwitharecipecataloguetohavenicherecipesthatonlyourusershaveaccessto.Oncethe\ufb01leisobtainedscrappingtheingredientstoarecipeispermi\\ed. 7.TechnologyProvideatechnicaldescripGonoftheapproachtheteamusedtoachieveitsproposedgoal,includingthewaysinwhichtheselectedAIplaVormsareusedwithintheprototypeandhowtheteamanGcipatesusingthoseandotherservicesintheMVPphase. Speci\ufb01cally,thedocumentaGonshouldincludealistofthecomponentsoftheselectedAIplaVormsthatareleveragedintheprototype,anyaddiGonalcomponentsthatmaybeleveragedinthedevelopmentoftheMVP,andaddiGonalservicesthatmaybenecessaryforconGnueddevelopment.Responseislimitedto350words. To\ufb01gureoutwhattypeofso]wareweneededtomakethisappareality,we\ufb01rstcreatedaprocedural\ufb02owchart.thisallowedustomapoutwhatfuncEonaliEeswewantedtheapptoencompassandhowweweregoingtoachievethis.The\ufb01rstpartoftheuserinterfaceasksforheight,weight,gender,acEvitylevel,andallergies.TheinformaEongatheredfromtheheight,weight,gender,andacEvitylevelwillthenbeusedinaformulafoundonHarvard.edutocalculatehowmanycalories,gramsofprotein,fats,andcarbsareneededperdaytoloseweightbasedontheuser\\'scurrentcondiEons.Theformulausedto\ufb01ndthisinformaEonwasoriginallycodedinPythonbutweplantoswitchallofourcodetoSwi]tobeabletouploadittotheappstore.Fortheuserinterface,weusedFigmatogenerateavisualforwhatwewantourUItolooklike.ToselecttherecipesfromtheinformaEoncalculatedwedecidedtouseawebscrapingalgorithminPythonwhichofcoursewillbeconvertedtoSwi]tobedevelopedintoanappontheAppStore.Tothengettheingredientsfromtheselectedrecipe,aPython\ufb01lescrapingalgorithmwillbeemployed.Forbothofthesescrapingalgorithms,thereareextensivePythonlibrarieswecanuseoruseasanexampletocreateourown.FinallytopersonalizetheAppaNeuralNetworkwillbeimplementedtohelprecommendrecipestotheuserthatarebasedontheirpreviousselecEons.Afeaturewewouldliketoimplementistheappwillaskforaweeklyweightupdatetorecalculatemacroandmicronutrientsandimprovetheapp\\'spersonalizaEonfeatures. 8.PrototypeVideoOverviewAllteamssubmiXngaprototypeforreviewarerequiredtosubmitvideodemonstraGonsoftheirworkingprototypes.Thevideosmust: \u2022benomorethan5minutesinlength.  \u2022explaintheintent,goals,andpotenGalimpactofthesoluGon. \u2022demonstratethebasic,workingfuncGonalityoftheprototype. \u2022beavailablethroughaYouTubelinkaccessibleforviewingbytheChallengereviewers. TheproducGonvalueofthevideoswillnotbefactoredintothereview,buttheymustclearlyandaccuratelyrepresenttheprototypefuncGonality.Tohelp, MediaCommonsatPennState providesfreeOneBu_onStudioopGonsthroughouttheCommonwealth. **SeeVideoProvidedintheFolder", "comments": "Project Name: 18 - Meal Prep Pro\nInnovation & Technical Merit (10 points): 5.0\nImpact & Relevance (10 points): 6.5\nUser Experience & Accessibility (10 points): 5.5\nEthical Considerations (10 points): 6.5\nFeasibility & Implementation (10 points): 6.0\nTotal Score (50 possible): 29.5\nComments to help explain your scores.: The idea is well explained but spends most of the time setting context and could spend more demonstrating a working prototype.   Technology is a good combination of existing tools to accomplish a feasible goal. 1. After reading the write up and watching the video, it was unclear to me what AI/ML techniques would be used.  As a reviewer, it would have helped me to have additional technical details."}
    '''

    example_3_lowest_score = '''
    {"submission": "2024Ni\\'anyAIChallengeSubmissionID:12TEAMINFORMATION 1.ProjectTeamName: SPECTRUMSTORIES 2.TeamMembers:ListeachteammemberincludingName,PSUEmail,Campus,andCollege(ex:JaneDoe,jxd123@psu.edu,Shenango,Engineering) SavithaKolar(svk3@psu.edu)andFrankLong(fvl5170@psu.edu),WorldCampus,MPSinAI. 3.PrimaryContact/TeamLead: SavithaKolar,svk3@psu.edu,814-753-1930PROJECTINFORMATION4.Problem/OpportunityStatementDocumentaGonshouldincludeanoverviewoftheproblemandthemethodusedtoaddressthatproblem.ThisshoulddemonstratethatyouclearlyunderstandtheproblemoropportunityyouareaddressingwithAI.Responseislimitedto300words. IntheUSAalone,anesQmated15-20percentoftheworld\\'spopulaQonexhibitssomeformofneurodivergence.NeurodiversitydescribesthevariaQoninthehumanexperienceoftheworld,inschool,atwork,andthroughsocialrelaQonships.BynotmakingbooksandeducaQonalmaterialaccessibleandinclusive,weareessenQallyignoringalargepartofthepopulaQonandleavingthemwithnomeanstoadvancetheireducaQonalskillsandbeindependent,funcQoningmembersofsociety. BydevelopinginclusivereadingmaterialandillustraQons,ourhopeistobringalivethemagicofclassics(tostartwith),andensureeducaQonalmaterialsaremoreinclusiveinnature. 5.MVPUseCaseProvideasampleusecaseforthetool.DescribehowsomeonewillusetheMVPfuncGonalityyouintendtobuildandthebene\ufb01tsorimpacttheMVPwillprovide.Responseislimitedto300words. AsaMinimumViableProduct,wechosethestoryofGoldilocksandtheThreeBearsasausecase.Forourprototype,wehaveidenA\ufb01ed10potenAalstepsingeneraAnganeurodivergent-friendlyillustraAonandstory.Theuserwould\ufb01rstselectastory,inthisexample,itwouldbeGoldilocksandtheThreeBears.Theywouldcopythetextofthestoryandinputitintoourapp. Theywouldthenselecttheneurodivergentsub-category,forinstance,AuAsmSpectrumDisorder,Dyslexia,etc.TheappwilluseNaturalLanguageProcessingtosummarize,tokenize,anduseNamed-enAtyRecogniAononthestorytext.Forexample,someenAAescouldbeGoldilocks,ThreeBears,etc.  TheappwillusethesetokensandenAAesthatwereextractedusingNLPinthepreviousprocessaspromptsintotheStableDi\ufb00usionAPIscript.TherewillalsobenegaAvepromptstoensurecleanerimages.TheappwillusecustomLoRAswhichareLowRankAdaptaAonsthatallowustouselow-rankadaptaAontechnologytoquickly\ufb01ne-tunedi\ufb00usionmodels.TheLoRAtrainingmodelmakesiteasiertotrainStableDi\ufb00usionondi\ufb00erentconcepts,suchascharactersoraspeci\ufb01cstyle.TheresponseofthestableDi\ufb00usionAPIscriptwilloutputthegeneratedimages.Thegeneratedimageswillbecombinedwiththetexttoproduceaneurodivergent-friendlystorybook. 6.DataAvailabilityDetailthedatasourcesleveragedwithintheprototypeaswellasthedatasourcesnecessaryifthisprojectmovedtoMVP.Ifavailable,pleasedetailthelocationandavailabilityofthedatasourcesand/ortheplanforcollectingthenecessarydata.Rememberthatwhilewecanprovidesomeassistancewithfindingdatasources,findingandgainingaccesstothosesourcesistheteam\\'sresponsibility.Responseislimitedto300words. ThedatasetweplantouseisfromwithinStableDi\ufb00usion,whichisbuilto\ufb00a5Billionimagepublicdataset.WeplantousestoriesthatareopensourceandfreelyavailablefromtheLibraryofcongress.WearealsoplanningtousepublicLoRAsfromCivitAI. 7.TechnologyProvideatechnicaldescripGonoftheapproachtheteamusedtoachieveitsproposedgoal,includingthewaysinwhichtheselectedAIplaVormsareusedwithintheprototypeandhowtheteamanGcipatesusingthoseandotherservicesintheMVPphase. Speci\ufb01cally,thedocumentaGonshouldincludealistofthecomponentsoftheselectedAIplaVormsthatareleveragedintheprototype,anyaddiGonalcomponentsthatmaybeleveragedinthedevelopmentoftheMVP,andaddiGonalservicesthatmaybenecessaryforconGnueddevelopment.Responseislimitedto350words. ThetechnologyweplanonusingtocreateSpectrumStorieswillinvolveNaturalLanguageProcessing(especiallythepartsinvolvingsummarizaQon,tokenizaQon,andNamedEnQtyRecogniQon)usingPythonastheprogramminglanguage.WewilluseStableDi\ufb00usionanditsAPIscriptalongwithcustomLoRAstogeneratetext-to-images. 8.PrototypeVideoOverviewAllteamssubmiXngaprototypeforreviewarerequiredtosubmitvideodemonstraGonsoftheirworkingprototypes.Thevideosmust: \u2022benomorethan5minutesinlength. \u2022explaintheintent,goals,andpotenGalimpactofthesoluGon. \u2022demonstratethebasic,workingfuncGonalityoftheprototype. \u2022beavailablethroughaYouTubelinkaccessibleforviewingbytheChallengereviewers. TheproducGonvalueofthevideoswillnotbefactoredintothereview,buttheymustclearlyandaccuratelyrepresenttheprototypefuncGonality.Tohelp, MediaCommonsatPennState providesfreeOneBu_onStudioopGonsthroughouttheCommonwealth. **SeeVideoProvidedintheFolder", "comments": "Project Name: 12 - SPECTRUM STORIES\nInnovation & Technical Merit (10 points): 4.5\nImpact & Relevance (10 points): 4.0\nUser Experience & Accessibility (10 points): 2.5\nEthical Considerations (10 points): 2.5\nFeasibility & Implementation (10 points): 4.5\nTotal Score (50 possible): 18.0\nComments to help explain your scores.: I think overall this is a neat idea, however the \"user\" role was not clearly defined, it was not clear where the team was gathering the necessary information to tailor the neuro-divergent category to, nor was their a feedback loop to ensure that the generated content aligned with the target audience.  There also wasn't any prototype, rather a flowchart for a process. The project is a nice integration of LLM and generative image technologies. No working prototype demonstrated, which limits overall scores.  Could further address ethical issues (e.g. potential for misuse of copyrighted material, consequences if software produces unsuitable imagery. \nRecommendations for the team to help them improve upon their prototype.: I'd recommend clearly defining the user role as this will impact everythign else.  My assumption was the \"user\" was a story creator.  If that is the case, how do they build out requirements for each neuro-divergent category?  How do they interact with the app/software?  Once a story is generated, how to they make sure in meetgs the needs of the targeted neuro-divergenct category?  How long does this entire process take, if they want to make 100's or 1000's of books.   Recommend sourcing training data from consenting authors and illustrators.  Recommend implementing system for feedback or remediation of generated imagery is unsuitable"}
    '''
    system_prompt = '''
        Pretend that you are a judge in the Nittany AI Challenge, an annual competition where college students propose innovative AI-driven solutions aimed at solving global issues across domains like education, health, the environment, and humanitarianism.
        Your role is to critically evaluate each prototype idea based on the specified criteria and scoring system to determine how effectively each team has leveraged AI to create meaningful impact.
    '''

    human_init_prompt_text = '''
        Hi there! I need your help to evaluate my prototype submission. Are you able to help me assess these prototypes and give feedback? I do not need scores.
    '''

    ai_init_prompt_text = '''
        Absolutely, I’d be glad to assist! With my expertise in AI and evaluating technical solutions, I can help you assess these prototypes in detail.
        Could you provide me with the specific criteria you’d like me to use for these evaluations?
    '''

    human_score_prompt_text = f'''
        Great! I will give you the criteria, but ignore the score because I do not need scores. Here is the criteria:\n{criteria}
    '''

    ai_example_prompt_text = '''
    Great, thank you for providing the detailed criteria. Could you provide three examples so I can assess your prototype accordingly?
    '''

    human_example_1_text = f'''
    Sure! Here is the first example from last year that got the highest score. {example_1_highest_score}
    '''

    ai_example_1_text = '''
    Thank you! Could you provide me the next one?
    '''

    human_example_2_text = f'''
    Yes! Here is the second example from last year that got an average score. {example_2_average_score}
    '''

    ai_example_2_text = '''
    Thank you! Could you provide me the last one?
    '''

    human_example_3_text = f'''
    Yes! Here is the last example from last year that got the lowest score. {example_3_lowest_score}
    '''
    ai_submission_prompt = f'''
    Thank you for providing the three examples! Now, could you submit your work? I will evaluate it based on the criteria you provided earlier and only give you the feedback without scores.
    '''
    
    # Call Azure OpenAI API to generate the evaluation
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": human_init_prompt_text},
            {"role": "system", "content": ai_init_prompt_text},
            {"role": "user", "content": human_score_prompt_text},
            {"role": "system", "content": ai_example_prompt_text},
            {"role": "user", "content": human_example_1_text},
            {"role": "system", "content": ai_example_1_text},
            {"role": "user", "content": human_example_2_text},
            {"role": "system", "content": ai_example_2_text},
            {"role": "user", "content": human_example_3_text},
            {"role": "system", "content": ai_submission_prompt},
            {"role": "user", "content": f"Sure, here is my submission: {submission_content}"},
        ],
        max_tokens=1500,
        temperature = 0
    )

    # Retrieve the generated evaluation
    evaluation = response.choices[0].message.content.strip()

    # Generate markdown file name based on project name
    markdown_filename = os.path.join(EVALUATIONS_OUTPUT_FOLDER, f"{project_name}_Evaluation.md")

    # Markdown template
    markdown_template = f"""
    # Evaluation for {project_name}

    ---

    {evaluation}

    ---

    """

    # Write the evaluation to the markdown file
    with open(markdown_filename, 'w', encoding="utf-8") as md_file:  # Specify UTF-8 encoding here
        md_file.write(markdown_template.strip())

# Function to check for new project folders, process each, and generate evaluations
def process_project_folders():
    # Load judging criteria
    criteria = load_judging_criteria()
    if not criteria:
        return

    # Get all project folders in the main project folder
    project_folders = [f for f in os.listdir(PROJECT_FOLDER) if os.path.isdir(os.path.join(PROJECT_FOLDER, f))]

    if not project_folders:
        print("No project folders found to process.")
        return

    # Process each project folder
    for folder_name in project_folders:
        project_path = os.path.join(PROJECT_FOLDER, folder_name)

        # Clean project name to remove the date suffix
        project_name = clean_project_name(folder_name)

        # Find the main submission file in the project folder (assuming .txt files are project descriptions)
        submission_files = [f for f in os.listdir(project_path) if f.endswith('.txt')]

        if not submission_files:
            print(f"No .txt files found in {project_path}. Skipping.")
            continue

        # Read the content of the first .txt file as the main submission
        submission_path = os.path.join(project_path, submission_files[0])
        with open(submission_path, 'r', encoding="utf-8") as f:
            submission_content = f.read()

        # Evaluate the submission using Azure OpenAI
        evaluate_submission(submission_content, project_name, criteria)

    print(f"Processed {len(project_folders)} project folders.")

if __name__ == "__main__":
    process_project_folders()
