# python script which writes several gmat scripts and then runs them all\n
# this is so I can make the colormap quickly.\n
# tckf 17-jan-2017\n
script  = """
%%General Mission Analysis Tool(GMAT) Script\n
%%Created: 2016-11-08 17:28:09\n
\n
\n
%%----------------------------------------\n
%%---------- Spacecraft\n
%%----------------------------------------\n
\n
Create Spacecraft DefaultSC;\n
GMAT DefaultSC.DateFormat = UTCGregorian;\n
GMAT DefaultSC.Epoch = '01 %s 2019 11:59:28.000';\n
GMAT DefaultSC.CoordinateSystem = EarthMJ2000Eq;\n
GMAT DefaultSC.DisplayStateType = Keplerian;\n
GMAT DefaultSC.SMA = 7191.938817629034;\n
GMAT DefaultSC.ECC = 0.02454974900598346;\n
GMAT DefaultSC.INC = %s;\n
GMAT DefaultSC.RAAN = 306.6148021947984;\n
GMAT DefaultSC.AOP = 314.1905515359963;\n
GMAT DefaultSC.TA = 99.88774933204458;\n
GMAT DefaultSC.DryMass = 10;\n
GMAT DefaultSC.Cd = 2.2;\n
GMAT DefaultSC.Cr = 1.8;\n
GMAT DefaultSC.DragArea = 0.0264;\n
GMAT DefaultSC.SRPArea = 1;\n
GMAT DefaultSC.NAIFId = -10000001;\n
GMAT DefaultSC.NAIFIdReferenceFrame = -9000001;\n
GMAT DefaultSC.OrbitColor = Red;\n
GMAT DefaultSC.TargetColor = Teal;\n
GMAT DefaultSC.EstimationStateType = 'Cartesian';\n
GMAT DefaultSC.OrbitErrorCovariance = [ 1e+70 0 0 0 0 0 ; 0 1e+70 0 0 0 0 ; 0 0 1e+70 0 0 0 ; 0 0 0 1e+70 0 0 ; 0 0 0 0 1e+70 0 ; 0 0 0 0 0 1e+70 ];\n
GMAT DefaultSC.CdSigma = 1e+70;\n
GMAT DefaultSC.CrSigma = 1e+70;\n
GMAT DefaultSC.Id = 'SatId';\n
GMAT DefaultSC.Attitude = CoordinateSystemFixed;\n
GMAT DefaultSC.SPADSRPScaleFactor = 1;\n
GMAT DefaultSC.ModelFile = 'aura.3ds';\n
GMAT DefaultSC.ModelOffsetX = 0;\n
GMAT DefaultSC.ModelOffsetY = 0;\n
GMAT DefaultSC.ModelOffsetZ = 0;\n
GMAT DefaultSC.ModelRotationX = 0;\n
GMAT DefaultSC.ModelRotationY = 0;\n
GMAT DefaultSC.ModelRotationZ = 0;\n
GMAT DefaultSC.ModelScale = 1;\n
GMAT DefaultSC.AttitudeDisplayStateType = 'Quaternion';\n
GMAT DefaultSC.AttitudeRateDisplayStateType = 'AngularVelocity';\n
GMAT DefaultSC.AttitudeCoordinateSystem = EarthMJ2000Eq;\n
GMAT DefaultSC.EulerAngleSequence = '321';\n
\n
\n
\n
\n
%%----------------------------------------\n
%%---------- ForceModels\n
%%----------------------------------------\n
\n
Create ForceModel DefaultProp_ForceModel;\n
GMAT DefaultProp_ForceModel.CentralBody = Earth;\n
GMAT DefaultProp_ForceModel.PrimaryBodies = {Earth};\n
GMAT DefaultProp_ForceModel.Drag = None;\n
GMAT DefaultProp_ForceModel.SRP = Off;\n
GMAT DefaultProp_ForceModel.RelativisticCorrection = Off;\n
GMAT DefaultProp_ForceModel.ErrorControl = RSSStep;\n
GMAT DefaultProp_ForceModel.GravityField.Earth.Degree = 4;\n
GMAT DefaultProp_ForceModel.GravityField.Earth.Order = 4;\n
GMAT DefaultProp_ForceModel.GravityField.Earth.PotentialFile = 'JGM2.cof';\n
GMAT DefaultProp_ForceModel.GravityField.Earth.EarthTideModel = 'None';\n
\n
%%----------------------------------------\n
%%---------- Propagators\n
%%----------------------------------------\n
\n
Create Propagator DefaultProp;\n
GMAT DefaultProp.FM = DefaultProp_ForceModel;\n
GMAT DefaultProp.Type = RungeKutta89;\n
GMAT DefaultProp.InitialStepSize = 60;\n
GMAT DefaultProp.Accuracy = 9.999999999999999e-12;\n
GMAT DefaultProp.MinStep = 0.001;\n
GMAT DefaultProp.MaxStep = 2700;\n
GMAT DefaultProp.MaxStepAttempts = 50;\n
GMAT DefaultProp.StopIfAccuracyIsViolated = true;\n
\n
%%----------------------------------------\n
%%---------- Coordinate Systems\n
%%----------------------------------------\n
\n
Create CoordinateSystem gse;\n
GMAT gse.Origin = Earth;\n
GMAT gse.Axes = GSE;\n
\n
%%----------------------------------------\n
%%---------- Subscribers\n
%%----------------------------------------\n
\n
Create OrbitView DefaultOrbitView;\n
GMAT DefaultOrbitView.SolverIterations = Current;\n
GMAT DefaultOrbitView.UpperLeft = [ 0.4336917562724014 0.04154302670623145 ];\n
GMAT DefaultOrbitView.Size = [ 0.992831541218638 0.9554896142433235 ];\n
GMAT DefaultOrbitView.RelativeZOrder = 32;\n
GMAT DefaultOrbitView.Maximized = true;\n
GMAT DefaultOrbitView.Add = {DefaultSC, Earth};\n
GMAT DefaultOrbitView.CoordinateSystem = EarthMJ2000Eq;\n
GMAT DefaultOrbitView.DrawObject = [ true true ];\n
GMAT DefaultOrbitView.DataCollectFrequency = 1;\n
GMAT DefaultOrbitView.UpdatePlotFrequency = 50;\n
GMAT DefaultOrbitView.NumPointsToRedraw = 0;\n
GMAT DefaultOrbitView.ShowPlot = true;\n
GMAT DefaultOrbitView.ShowLabels = true;\n
GMAT DefaultOrbitView.ViewPointReference = Earth;\n
GMAT DefaultOrbitView.ViewPointVector = [ 30000 0 0 ];\n
GMAT DefaultOrbitView.ViewDirection = Earth;\n
GMAT DefaultOrbitView.ViewScaleFactor = 1;\n
GMAT DefaultOrbitView.ViewUpCoordinateSystem = EarthMJ2000Eq;\n
GMAT DefaultOrbitView.ViewUpAxis = Z;\n
GMAT DefaultOrbitView.EclipticPlane = Off;\n
GMAT DefaultOrbitView.XYPlane = On;\n
GMAT DefaultOrbitView.WireFrame = Off;\n
GMAT DefaultOrbitView.Axes = On;\n
GMAT DefaultOrbitView.Grid = Off;\n
GMAT DefaultOrbitView.SunLine = Off;\n
GMAT DefaultOrbitView.UseInitialView = On;\n
GMAT DefaultOrbitView.StarCount = 7000;\n
GMAT DefaultOrbitView.EnableStars = On;\n
GMAT DefaultOrbitView.EnableConstellations = On;\n
\n
Create GroundTrackPlot DefaultGroundTrackPlot;\n
GMAT DefaultGroundTrackPlot.SolverIterations = Current;\n
GMAT DefaultGroundTrackPlot.UpperLeft = [ 0.4336917562724014 0.04154302670623145 ];\n
GMAT DefaultGroundTrackPlot.Size = [ 0.992831541218638 0.9554896142433235 ];\n
GMAT DefaultGroundTrackPlot.RelativeZOrder = 12;\n
GMAT DefaultGroundTrackPlot.Maximized = true;\n
GMAT DefaultGroundTrackPlot.Add = {DefaultSC};\n
GMAT DefaultGroundTrackPlot.DataCollectFrequency = 1;\n
GMAT DefaultGroundTrackPlot.UpdatePlotFrequency = 50;\n
GMAT DefaultGroundTrackPlot.NumPointsToRedraw = 0;\n
GMAT DefaultGroundTrackPlot.ShowPlot = true;\n
GMAT DefaultGroundTrackPlot.CentralBody = Earth;\n
GMAT DefaultGroundTrackPlot.TextureMap = 'ModifiedBlueMarble.jpg';\n
\n
Create ReportFile ReportFile1;\n
GMAT ReportFile1.SolverIterations = Current;\n
GMAT ReportFile1.UpperLeft = [ 0 0 ];\n
GMAT ReportFile1.Size = [ 0 0 ];\n
GMAT ReportFile1.RelativeZOrder = 0;\n
GMAT ReportFile1.Maximized = false;\n
GMAT ReportFile1.Filename = 'ReportFile1.txt';\n
GMAT ReportFile1.Precision = 16;\n
GMAT ReportFile1.Add = {DefaultSC.A1ModJulian, DefaultSC.EarthMJ2000Eq.X, DefaultSC.gse.X, DefaultSC.gse.Y, DefaultSC.gse.Z};\n
GMAT ReportFile1.WriteHeaders = true;\n
GMAT ReportFile1.LeftJustify = On;\n
GMAT ReportFile1.ZeroFill = Off;\n
GMAT ReportFile1.FixedWidth = false;\n
GMAT ReportFile1.Delimiter = ',';\n
GMAT ReportFile1.ColumnWidth = 23;\n
GMAT ReportFile1.WriteReport = true;\n
\n
\n
%%----------------------------------------\n
%%---------- Mission Sequence\n
%%----------------------------------------\n
\n
BeginMissionSequence;\n
Propagate DefaultProp(DefaultSC) {DefaultSC.ElapsedDays = 90};\n
"""
from subprocess import call

# for now this can only be run from the GMAT scripts folder
# this does the basics so the next thing to do is to 


# i'm seeing a great opportunity to use "map" here
output_location = "../output/"
data_destination = "/home/tckf/BostonUniversity/research/data-se3-path-planner/yearData/batch2019/"


scriptname = "test.script"
f=open(scriptname,'w')
test = 'Jan'
inc = '65'
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
            'Oct', 'Nov', 'Dec']
inclinations = [float(55+5*i) for i in range(0,8)]
inclinations = inclinations[::]
batch = [[script%(month,inclination) for month in months] for inclination in inclinations]
# batch = [[script%(month,inclination) for month in months] for inclination in inclinations]
f.write(batch)
f.close()

# here's the part where I'm actually trying to run stuff
# call(["./GmatConsole-R2016a", scriptname])
# call(["mv", output_location+"ReportFile1.txt", data_destination+"test.csv"])
# call(["rm", scriptname])


