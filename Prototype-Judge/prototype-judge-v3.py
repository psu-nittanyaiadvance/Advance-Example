import openai
import os
from dotenv import load_dotenv
import openai
from PyPDF2 import PdfReader
import re

rubric = '''
"1. Innovation and Technical Merit"
   """- Questions to consider:
     1. Does the prototype demonstrate a novel use of AI, or does it improve upon existing solutions in a significant way?
     2. Is the underlying AI model robust, accurate, and efficient?
     3. How well has the team addressed potential technical challenges and limitations of their solution?
   - Strongly Disagree (1-2 points): The prototype offers a rudimentary application of AI with no clear novel approach or improvement on existing systems.
   - Disagree (3-4 points): The prototype applies AI in a somewhat unique manner but still largely aligns with existing solutions.
   - Neither Agree nor Disagree (5-6 points): The prototype demonstrates a fresh approach to the problem, with evidence of technical proficiency.
   - Agree (7-8 points): The prototype showcases advanced AI methods and provides significant improvements over current solutions.
   - Strongly Agree (9-10 points): The prototype is groundbreaking, pushing the boundaries of current AI capabilities and offering transformative advancements."""

"2. Impact and Relevance"
   """- Questions to consider:
     1. Does the prototype address a pressing or significant issue within its chosen area (education, environment, humanitarianism, health)?
     2. How scalable is the solution, and what potential does it have to create widespread positive change?
     3. Is there clear evidence or data supporting the prototype's potential impact?
   - Strongly Disagree (1-2 points): The prototype addresses a minor or vague issue, with limited potential for meaningful impact.
   - Disagree (3-4 points): The prototype tackles a recognized issue but may lack the scope or depth for substantial change.
   - Neither Agree nor Disagree (5-6 points): The prototype addresses a significant issue, with potential for noticeable positive change.
   - Agree (7-8 points): The prototype targets a major problem, with plans that could lead to widespread positive impact.
   - Strongly Agree (9-10 points): The prototype addresses a critical issue, demonstrating a clear path to transformative change in the chosen area."""

"3. User Experience and Accessibility"
   """- Questions to consider:
     1. Is the prototype user-friendly, intuitive, and accessible to a diverse range of users, including those with disabilities?
     2. How well has the team considered the cultural, socio-economic, and demographic differences of potential users?
     3. Are there mechanisms in place to collect user feedback and iterate upon it?
   - Strongly Disagree (1-2 points): The prototype is difficult to navigate, lacks accessibility features, and has not considered diverse user needs.
   - Disagree (3-4 points): The prototype has basic user-friendliness but misses several key accessibility or inclusivity elements.
   - Neither Agree nor Disagree (5-6 points): The prototype offers a satisfactory user experience and includes some accessibility features.
   - Agree (7-8 points): The prototype provides an intuitive user experience, catering to a broad range of users and diverse needs.
   - Strongly Agree (9-10 points): The prototype excels in user experience, ensuring full accessibility and inclusivity, with strong evidence of user testing and feedback."""

"4. Ethical Considerations"
   """- Questions to consider:
     1. How well does the prototype address potential ethical concerns, including data privacy, fairness, and transparency?
     2. Is there a plan in place to handle unintended consequences or misuse of the technology?
     3. Has the team demonstrated an understanding of the broader societal implications of their solution?
   - Strongly Disagree (1-2 points): The prototype lacks any consideration for ethical implications, with clear potential issues.
   - Disagree (3-4 points): The prototype acknowledges some ethical aspects but lacks comprehensive planning or solutions.
   - Neither Agree nor Disagree (5-6 points): The prototype demonstrates an awareness of ethical concerns and has made efforts to address them.
   - Agree (7-8 points): The prototype shows a deep understanding of ethical considerations, with a robust plan to address potential issues.
   - Strongly Agree (9-10 points): The prototype exemplifies best practices in AI ethics, from data handling to broader societal implications, with a clear commitment to ongoing ethical evaluation."""

"5. Feasibility and Implementation"
   """- Questions to consider:
     - How realistic is the prototype's implementation in real-world scenarios?
     - Is there a clear roadmap for moving from the prototype stage to full deployment?
     - Has the team considered the economic, infrastructural, and regulatory challenges of their solution?
   - Strongly Disagree (1-2 points): The prototype seems impractical for real-world implementation, with numerous unaddressed challenges.
   - Disagree (3-4 points): The prototype has potential but lacks a clear plan for addressing major barriers to deployment.
   - Neither Agree nor Disagree (5-6 points): The prototype is feasible for certain scenarios, with some plans to overcome potential challenges.
   - Agree (7-8 points): The prototype demonstrates strong feasibility, with a comprehensive plan for broader implementation.
   - Strongly Agree (9-10 points): The prototype is highly feasible, backed by a detailed roadmap, partnerships, or resources, ensuring successful real-world deployment."""
'''
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
    Hi there! I need your help to evaluate my prototype submission. Are you able to help me assess these prototypes systematically?
'''

ai_init_prompt_text = '''
    Absolutely, I’d be glad to assist! With my expertise in AI and evaluating technical solutions, I can help you assess these prototypes in detail.
    Could you provide me with the specific criteria you’d like me to use for these evaluations?
'''

human_score_prompt_text = f'''
    Great! Here is the criteria:\n{rubric}
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
Thank you for providing the three examples! Now, could you submit your work? I will evaluate it based on the criteria you provided earlier.
'''

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

openai.api_type = "azure"
openai.api_base = endpoint 
openai.api_version = "2024-08-01-preview"  # Adjust the version based on your Azure resource setup
openai.api_key = api_key 
model = "gpt-4o"


def judge_submission(submission):
    response = openai.ChatCompletion.create(
        deployment_id="gpt-4o",
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
            {"role": "user", "content": f"Sure, here is my submission: {submission}"},
        ],
        max_tokens=1000,
        temperature = 0
    )
    return response['choices'][0]['message']['content']

def extract_text(filename):
    try:
        reader = PdfReader(filename)
        full_text = ""

        for page in reader.pages:
            text = page.extract_text() or ""
            text = re.sub(r'(?<=\S) (?=\S)', '', text)  # Remove spaces between letters
            text = re.sub(r'\s+', ' ', text)  # Remove extra spaces between words
            
            # Normalize quotes if needed
            text = text.replace('“', '"').replace('”', '"')  # Normalize double quotes
            text = text.replace("‘", "'").replace("’", "'")  # Normalize single quotes
            text = text.replace('"', '\\"').replace("'", "\\'")
            text = text.replace('\n', '\\n') 

            full_text += text + " "

        return full_text.strip()  # Trim any trailing spaces

    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return None
    
def create_json(submission, comments):
    # criteria = """
    #         I would like you to evaluate an AI-based prototype idea using five key criteria: 
    #         1. Impact (10 points)
    #         2. Feasibility (10 points)
    #         3. Implementation & Scaling (10 points)
    #         4. Team Capabilities (10 points)
    #         5. Technical Sophistication (10 points)
    #         6. Use of AI & ML Technologies (5 points)
    #         7. Use of Available Data (5 points)
    #         8. Interface Design Plans/Consumability (5 points)
    #         For each criterion, I need scores from 1 to 10 or 1 to 5 (The higher number, the better, 65 points in total). 
    #         Here is the submission:
    #         """
    # prompt = criteria + submission
    completion = comments
    json = {"prompt": submission, "completion": completion}
    return json


if __name__=="__main__":

    directory = 'Prototype-Judge/challenge-data/2023-top10'
    # test_directory = 'Prototype-Judge/challenge-data/2023-top10-test'
    test_directory = 'Prototype-Judge/challenge-data/prototype-judge-2024/2024-test'
    pdf_paths_list = []
    test_pdf_paths_list = []

    pdf_files_list = []
    test_pdf_files_list = []

    judge_comments = None
    json_list = []

    for filename in os.listdir(directory):
        if filename.endswith('.pdf'):  
            joined_path = os.path.join(directory, filename)
            pdf_paths_list.append(os.path.normpath(joined_path))

    for filename in os.listdir(test_directory):
        if filename.endswith('.pdf'):  
            test_joined_path = os.path.join(test_directory, filename)
            test_pdf_paths_list.append(os.path.normpath(test_joined_path))

    for pdf_file_path in pdf_paths_list:
        pdf_files_list.append(extract_text(pdf_file_path))

    for test_pdf_file_path in test_pdf_paths_list:
        test_pdf_files_list.append(extract_text(test_pdf_file_path))

    with open('Prototype-Judge/challenge-data/2023-top10/2023-judge-comments.txt', 'r') as filename:
        judge_comments = filename.read()

    judge_comments_list = judge_comments.split('\n\n')

    for pdf, judge_comment in zip(pdf_files_list, judge_comments_list):
        json_object = judge_comment
        #create_json(pdf, judge_comment)
        json_list.append(json_object)

    result_list = []
    # for json_object, test_pdf in zip(json_list, test_pdf_files_list):
    #     result_list.append(judge_submission(json_object, test_pdf))

    # manually change the input
    result_list.append(judge_submission(test_pdf_files_list[0]))

    with open("Prototype-Judge/judge_output_AdvIsor_withExamples.txt", "w") as file:
        for result in result_list:
            file.write(result + "\n")

    print("Output saved to judge_output.txt")