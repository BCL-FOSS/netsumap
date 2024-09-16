package com.bcl.netifidash.util;

import com.codename1.components.ToastBar;
import com.codename1.io.rest.Response;
import com.codename1.io.rest.Rest;
import com.codename1.ui.Dialog;
import com.google.gson.Gson;


import java.util.LinkedHashMap;
import java.util.Map;

public class BackendUtil {

    public BackendUtil (){}

    public void connect(String nd_ip, String nd_port, String ip, String port, String user, String pass){

        String baseURL = "http://"+nd_ip+":"+nd_port;

        Map<String, String> json = new LinkedHashMap<>();
        json.put("port", port);
        json.put("ip", ip);
        json.put("username", user);
        json.put("password", pass);

        //System.out.println(json.toString());

        Response<Map> result = Rest.post(baseURL+"/login").
                contentType("application/json").body(json.toString())
                .getAsJsonMap();

        if(result.getResponseData() != null) {
            String error = (String)result.getResponseData().get("error_message");
            if(error != null) {
                Dialog.show("UniFi Connection Error", error, "OK", null);
            }
        } else {
            Dialog.show("UniFi Connection Successful", result.getResponseData().toString(), "OK", null);
        }
    }

    public void auth(){

        Response<Map> result = Rest.post("http://107.191.44.222:25000/unifi_webhook").
                contentType("application/json").body("{\"unifi_alarm\" : \"from_mobile_app\"}")
                .getAsJsonMap();


        if(result.getResponseData() != null) {
            String error = (String)result.getResponseData().get("error_message");
            if(error != null) {
                ToastBar.showErrorMessage(error);
            }
        } else {
            ToastBar.showErrorMessage("Error connecting to Backend API: " + result.getResponseCode());
        }

    }

    public void wsConnection(){





    }
}
