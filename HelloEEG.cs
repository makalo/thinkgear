using System;
using System.Diagnostics;
using System.Text;
using System.Threading;
using System.Reflection;
using System.Net;
using System.Net.Sockets;
using NeuroSky.ThinkGear;
using System.Windows.Forms;

namespace testprogram
{
    class Program {
        static byte[] buffer = new byte[16];
        static Socket tcp1;
        static Socket tcp2;
        static int flag = 0;
        static int flag1 = 0;
        static int y = 0;
        static int x = 0;
        static int tag = 0;
        static Connector connector;
        static int num=0;
        static bool golfZoneDemo = false;
        static double task_famil_baseline, task_famil_cur, task_famil_change;
        static bool task_famil_first;
        static double mental_eff_baseline, mental_eff_cur, mental_eff_change;
        static bool mental_eff_first;

        public static void Main(string[] args) {

            Assembly assembly = System.Reflection.Assembly.GetExecutingAssembly();
            if (assembly != null)
            {
                object[] customAttribute1 = assembly.GetCustomAttributes(typeof(AssemblyTitleAttribute), false);
                if ((customAttribute1 != null) && (customAttribute1.Length > 0))
                    Console.WriteLine(((AssemblyTitleAttribute)customAttribute1[0]).Title);
                object[] customAttribute2 = assembly.GetCustomAttributes(typeof(AssemblyCompanyAttribute), false);
                if ((customAttribute2 != null) && (customAttribute2.Length > 0))
                    Console.WriteLine(((AssemblyCompanyAttribute)customAttribute2[0]).Company);
                Console.WriteLine(assembly.GetName().Version.ToString());
                
            }
            AppDomain MyDomain = AppDomain.CurrentDomain;
            Assembly[] AssembliesLoaded = MyDomain.GetAssemblies();

            foreach (Assembly MyAssembly in AssembliesLoaded)
            {
                if (MyAssembly.FullName.Contains("ThinkGear"))
                    Console.WriteLine(MyAssembly.FullName);
                
            }

            
            Console.WriteLine("----------");
            if (golfZoneDemo) Console.WriteLine("Hello Golfer!");
            else Console.WriteLine("Hello EEG!");
            Console.WriteLine("----------");

            // Initialize a new Connector and add event handlers
            Thread t1 = new Thread(new ThreadStart(snake));
            t1.Start();
            connector = new Connector();
            connector.DeviceConnected += new EventHandler(OnDeviceConnected);
            connector.DeviceConnectFail += new EventHandler(OnDeviceFail);
            connector.DeviceValidating += new EventHandler(OnDeviceValidating);

            connector.ConnectScan("COM17");
            
            //start the mental effort and task familiarity calculations
            if (golfZoneDemo) {
                connector.setMentalEffortEnable(false);
                connector.setTaskFamiliarityEnable(false);
                connector.setBlinkDetectionEnabled(false);
            }
            else {
                connector.enableTaskDifficulty(); //depricated
                connector.enableTaskFamiliarity(); //depricated

                connector.setMentalEffortRunContinuous(true);
                connector.setMentalEffortEnable(true);
                connector.setTaskFamiliarityRunContinuous(true);
                connector.setTaskFamiliarityEnable(true);

                connector.setBlinkDetectionEnabled(true);
            }
            task_famil_baseline = task_famil_cur = task_famil_change = 0.0;
            task_famil_first = true;
            mental_eff_baseline = mental_eff_cur = mental_eff_change = 0.0;
            mental_eff_first = true;
            


            Thread.Sleep(80 * 60 * 1000); // time to live for this program (8 min * 60 sec * 1000 ms)

            Console.WriteLine("----------"); 
            if (golfZoneDemo) Console.WriteLine("Time is up. Goodbye from Golf Zone sample program!");
            else Console.WriteLine("Time is up. Goodbye from EEG sample program!");
            Console.WriteLine("----------");

            // Close all open connections
            connector.Close();

            Thread.Sleep(10 * 1000); // delay long enough for a human to see the message (10 sec * 1000 ms)

            Environment.Exit(0);
        }

       
        /**
         * Called when a device is connected 
         */
        static void OnDeviceConnected(object sender, EventArgs e) {
            Console.WriteLine("wwwww");


            //Thread t1 = new Thread(new ThreadStart(snake));
            // t1.Start();
            Thread.Sleep(10000);//睡眠500毫秒，也就是0.5秒
            IPAddress ip = IPAddress.Parse("127.0.0.1");
            tcp1 = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            tcp2 = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            tcp1.Connect(new IPEndPoint(ip, 9999));
            tcp2.Connect(new IPEndPoint(ip, 9999));
           
            Thread t2 = new Thread(new ThreadStart(tcp2_feed));
            t2.Start();

            buffer[0]= 90;
            buffer[1] = 8;
            Connector.DeviceEventArgs de = (Connector.DeviceEventArgs)e;

            Console.WriteLine("Device found on: " + de.Device.PortName);
            
            de.Device.DataReceived += new EventHandler(OnDataReceived);
            Console.WriteLine("ppppppp");
        }
        static void tcp2_feed()
        {
            
            while(true)
            {
                tcp2.Receive(buffer);
                Console.WriteLine(buffer[0]+buffer[1]);
            }
            
        }
        static void snake()
        {
            Process p = Process.Start("snake.exe");
            p.WaitForExit();
        }
        static void Form1_KeyDown()
        {
            //Ctrl +F4关闭
           //f (Console.ReadKey() == ConsoleKey.F10)
             // Console.Write("F10 ");
        }

        /**
         * Called when scanning fails
         */
        static void OnDeviceFail(object sender, EventArgs e) {
            Console.WriteLine("No devices found! :(");
        }

        /**
         * Called when each port is being validated
         */ 
        static void OnDeviceValidating(object sender, EventArgs e) {
            Console.WriteLine("Validating: ");
        }

        static byte rcv_poorSignal_last = 255; // start with impossible value
        static byte rcv_poorSignal;
        static byte rcv_poorSig_cnt = 0;

        /**
         * Called when data is received from a device
         */
        static void OnDataReceived(object sender, EventArgs e) {
            //Device d = (Device)sender;
            Device.DataEventArgs de = (Device.DataEventArgs)e;
            DataRow[] tempDataRowArray = de.DataRowArray;
            string mybyte;
            TGParser tgParser = new TGParser();
            tgParser.Read(de.DataRowArray);
            
            //Console.WriteLine(buffer[0] + buffer[1]);
            //if (buffer=='1')
            //{
            //    Console.WriteLine("wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww");
            //}
            /* Loop through new parsed data */
            for (int i = 0; i < tgParser.ParsedData.Length; i++)
            {
                if (tgParser.ParsedData[i].ContainsKey("MSG_MODEL_IDENTIFIED"))
                {
                    Console.WriteLine("Model Identified");
                    connector.setMentalEffortRunContinuous(true);
                    connector.setMentalEffortEnable(true);
                    connector.setTaskFamiliarityRunContinuous(true);
                    connector.setTaskFamiliarityEnable(true);
                    connector.setPositivityEnable(false);
                    //
                    // the following are included to demonstrate the overide messages
                    //
                    connector.setRespirationRateEnable(true); // not allowed with EEG
                    connector.setPositivityEnable(true);// not allowed when famil/diff are enabled
                }
                if (tgParser.ParsedData[i].ContainsKey("PoorSignal"))
                {
                    // NOTE: this doesn't work well with BMD sensors Dual Headband or CardioChip

                    rcv_poorSignal = (byte)tgParser.ParsedData[i]["PoorSignal"];
                    if (rcv_poorSignal != rcv_poorSignal_last || rcv_poorSig_cnt >= 30)
                    {
                        // when there is a change of state OR every 30 reports
                        rcv_poorSig_cnt = 0; // reset counter
                        rcv_poorSignal_last = rcv_poorSignal;
                        if (rcv_poorSignal == 0)
                        {
                            // signal is good, we are connected to a subject
                            Console.WriteLine("SIGNAL: we have good contact with the subject");
                            mybyte = "9";
                            tcp2.Send(Encoding.UTF8.GetBytes(mybyte));
                            //tcpClient1.Send(Encoding.UTF8.GetBytes(mybyte), mybyte.Length, ipEndPoint);
                        }
                        else
                        {
                            Console.WriteLine("SIGNAL: is POOR: " + rcv_poorSignal);
                            mybyte ="8";
                            tcp2.Send(Encoding.UTF8.GetBytes(mybyte));
                            //udpClient.Send(Encoding.UTF8.GetBytes(mybyte), mybyte.Length, ipEndPoint);
                        }
                    }
                    else rcv_poorSig_cnt++;
                }
                
                
                if (tgParser.ParsedData[i].ContainsKey("Meditation"))
                {
                    if (tgParser.ParsedData[i]["Meditation"] != 0)
                    {
                        
                        Console.WriteLine("Meditation: " + tgParser.ParsedData[i]["Meditation"]);
                        
                        if (tgParser.ParsedData[i]["Meditation"]>100)
                        {
                            tag = 4;
                        }
                        if (tgParser.ParsedData[i]["Meditation"] < 20)
                        {
                            tag = 6;
                        }
                        y = (int)tgParser.ParsedData[i]["Meditation"];
                    }      
                        
                }
                if (tgParser.ParsedData[i].ContainsKey("Attention"))
                {
                    if (tgParser.ParsedData[i]["Attention"] != 0)
                    {
                        
                        Console.WriteLine("Attention : " + tgParser.ParsedData[i]["Attention"]);
                        flag = 0;
                        flag1 = 0;
                        num++;
                        if (tgParser.ParsedData[i]["Attention"] > 90)
                        {
                            tag = 5;
                        }
                        x = (int)tgParser.ParsedData[i]["Attention"];
                    }
                       
                }
                if (!golfZoneDemo) // turn this off for the Golf Zone Demo
                {
                    if (tgParser.ParsedData[i].ContainsKey("BlinkStrength"))
                    {
                        if (tgParser.ParsedData[i]["BlinkStrength"]> 55)
                        {
                            Console.WriteLine("\t\tBlinkStrength: " + tgParser.ParsedData[i]["BlinkStrength"]);
                            if (num>=2)
                            {
                                flag++;
                                num = 0;
                            }
                            flag1++;
                            if (buffer[0]+buffer[1]==97)
                            {
                                
                                if (flag1 == 1)
                                {
                                    Console.WriteLine("KKKKKKKKKK");
                                    mybyte = "1";
                                    tcp2.Send(Encoding.UTF8.GetBytes(mybyte));
                                    //udpClient.Send(Encoding.UTF8.GetBytes(mybyte), mybyte.Length, ipEndPoint2);
                                }
                            }
                            else if(buffer[0] + buffer[1] == 98)
                            {
                               
                                if (flag == 1 && flag1 == 1)
                                {
                                    Console.WriteLine("KKKKKKKKKK");
                                    mybyte = "1";
                                    tcp2.Send(Encoding.UTF8.GetBytes(mybyte));
                                    //udpClient.Send(Encoding.UTF8.GetBytes(mybyte), mybyte.Length, ipEndPoint2);
                                }
                            }
                            
                        }
                        
                    }
                }
                
                if ((x > 0 && y > 0) || tag>0)
                {
                    
                    mybyte = x * 10000 + y*10+tag + "";
                    tcp1.Send(Encoding.UTF8.GetBytes(mybyte));
                    //udpClient.Send(Encoding.UTF8.GetBytes(mybyte), mybyte.Length, ipEndPoint);
                    x = 0;
                    y = 0;
                    tag = 0;
                }
            }
        }



        static double calcPercentChange(double baseline, double current)
        {
            double change;

            if (baseline == 0.0) baseline = 1.0; //don't allow divide by zero
            /*
             * calculate the percentage change
             */
            change = current - baseline;
            change = (change / baseline) * 1000.0 + 0.5;
            change = Math.Floor(change) / 10.0;
            return (change);
        }
    }
}
