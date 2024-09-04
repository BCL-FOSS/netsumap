package com.bcl.netifidash.util;

import com.codename1.components.ToastBar;
import com.codename1.io.ConnectionRequest;
import com.codename1.io.rest.Response;
import com.codename1.io.rest.Rest;

import java.net.http.WebSocket;
import java.nio.ByteBuffer;
import java.util.Map;
import java.util.concurrent.CompletableFuture;

public class BackendUtil {
    public BackendUtil (){

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
