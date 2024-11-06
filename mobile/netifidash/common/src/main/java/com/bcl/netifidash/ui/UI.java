package com.bcl.netifidash.ui;

import com.codename1.io.Preferences;
import com.codename1.ui.*;
import com.codename1.ui.layouts.BoxLayout;
import com.codename1.ui.util.UITimer;
import com.bcl.netifidash.util.BackendUtil;

public class UI {

    private final BackendUtil backendUtil;

    public UI (){
        this.backendUtil = new BackendUtil();
    }

    public void splashScreen(){
        String isConfigured = Preferences.get("is_configured", "");
        Form main = new Form("", BoxLayout.y());
        String configCheck = "SET";
        TextArea name = new TextArea();
        name.setText("Welcome to NetiFiDash");
        main.add(name);
        main.show();

        if (isConfigured.equalsIgnoreCase(configCheck)) {
            new UITimer(() -> {
                Form mainApp = home();
                mainApp.show();
            }).schedule(3000, false, main);
        } else {
            new UITimer(() -> {
                Form initApp = setup();
                initApp.show();
            }).schedule(3000, false, main);
        }
    }

    public Form setup(){
        Form setup = new Form("Setup", BoxLayout.y());
        Button ubiquipyConnect = new Button("Connect");
        TextField ndIP = new TextField("net-con.ai Node Hostname/IP");
        TextField ndPort = new TextField("net-con.ai Node Port");
        TextField controllerIP = new TextField("Controller Hostname/IP");
        TextField controllerPort = new TextField("Controller Port");
        TextField userName = new TextField("Controller Username");
        TextField passWord = new TextField("Controller Password");
        Slider progress = new Slider();

        ubiquipyConnect.addActionListener(e -> this.backendUtil.connect(ndIP.getText(), ndPort.getText(), controllerIP.getText(), controllerPort.getText(),
                userName.getText(), passWord.getText(), progress));

        setup.add(ndIP);
        setup.add(ndPort);
        setup.add(controllerIP);
        setup.add(controllerPort);
        setup.add(userName);
        setup.add(passWord);
        setup.add(ubiquipyConnect);
        setup.add(progress);

        return setup;
    }

    public Form home(){
        Form home = new Form("Home", BoxLayout.y());
        Button socketTest = new Button("Send message to backend");
        TextField eventType = new TextField("Enter Event Type");
        TextField eventMessage = new TextField("Enter Event Message");
        TextField socketHost = new TextField("Enter Socket IP/Hostname");
        TextField socketPort = new TextField("Enter Socket Port");
        home.add(socketHost);
        home.add(socketPort);
        home.add(eventType);
        home.add(eventMessage);
        socketTest.addActionListener(e -> nocDash());
        home.add(socketTest);
        setMenu(home);
        return home;
    }

    public void nocDash(){
        Form noc = new Form("Dashboard", BoxLayout.y());
        setMenu(noc);
        noc.show();
    }

    public void net_dev_mgmt(){
        Form netDev = new Form("Network Devices", BoxLayout.y());
        setMenu(netDev);
        netDev.show();
    }

    public void client_mgmt(){
        Form usrDev = new Form("Client Devices", BoxLayout.y());
        setMenu(usrDev);
        usrDev.show();
    }

    public void setMenu(Form form){
        form.getToolbar().addMaterialCommandToSideMenu("Home",
                FontImage.MATERIAL_CHECK_CIRCLE_OUTLINE, 6, e -> home().show());
        form.getToolbar().addMaterialCommandToSideMenu("Dashboard",
                FontImage.MATERIAL_CHECK_CIRCLE_OUTLINE, 6, e -> nocDash());
        form.getToolbar().addMaterialCommandToSideMenu("Network Status",
                FontImage.MATERIAL_CHECK_CIRCLE_OUTLINE, 6, e -> net_dev_mgmt());
        form.getToolbar().addMaterialCommandToSideMenu("",
                FontImage.MATERIAL_CHECK_CIRCLE_OUTLINE, 6, e -> client_mgmt());
    }
}
