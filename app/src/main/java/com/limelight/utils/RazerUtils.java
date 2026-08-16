package com.limelight.utils;

import android.content.Context;
import android.graphics.Point;
import android.util.DisplayMetrics;
import android.util.Log;
import android.view.WindowManager;

import com.limelight.LimeLog;
import com.limelight.nvstream.StreamConfiguration;

/**
 * Description
 * Date: 2025-01-08
 */
public class RazerUtils {

    public static String getUrlParams(StreamConfiguration streamConfig){
        if(streamConfig.getRrazerVD()==0){
            return "";
        }
        //基地班sunshine  useVdd 1:0
        //appllo 虚拟显示器 virtualDisplay 1:0
        //雷蛇虚拟显示器 virtualDisplay 1扩展模式 2仅虚拟显示器 0不使用
        //timeToTerminateApp 0立即关闭 -1永不 300五分钟
        StringBuffer sb=new StringBuffer();
        //"&virtualDisplay=2&virtualDisplayMode=2400x1080x120&devicenickname=G's Redmi K40&ppi=393&screen_resolution=2400x1080&timeToTerminateApp=0&UIScale=150"+
        sb.append("&");
        sb.append("virtualDisplay=");
        sb.append(streamConfig.getRrazerVD());
        sb.append("&");
        sb.append("virtualDisplayMode=");
        sb.append(streamConfig.getWidth());
        sb.append("x");
        sb.append(streamConfig.getHeight());
        sb.append("x");
        sb.append(streamConfig.getRefreshRate());
        sb.append("&");
        sb.append("devicenickname=");
        sb.append(DeviceUtils.getManufacturer()+"-"+DeviceUtils.getModel());
        sb.append("&");
        sb.append("ppi=");
        sb.append(streamConfig.getPpi());
        sb.append("&");
        sb.append("screen_resolution=");
        sb.append(streamConfig.getWidth());
        sb.append("x");
        sb.append(streamConfig.getHeight());
        sb.append("&");
        sb.append("timeToTerminateApp=-1");
        sb.append("&");
        sb.append("UIScale=");
        sb.append("200");
        LimeLog.info("axixi:"+sb.toString());
        return sb.toString();
    }


    // 获取屏幕对角线尺寸（单位：英寸）
    public static double getDiagonalInches(Context context) {
        try {
            DisplayMetrics displayMetrics = context.getResources().getDisplayMetrics();
            Point screenResolution = getScreenResolution(context);
            int width = screenResolution.x;
            int height = screenResolution.y;

            float xdpi = displayMetrics.xdpi > 0 ? displayMetrics.xdpi : displayMetrics.densityDpi;
            float ydpi = displayMetrics.ydpi > 0 ? displayMetrics.ydpi : displayMetrics.densityDpi;

            double wi = width / (double) xdpi;
            double hi = height / (double) ydpi;
            double x = Math.pow(wi, 2.0);
            double y = Math.pow(hi, 2.0);

            return Math.round(Math.sqrt(x + y) * 10.0) / 10.0;
        } catch (Exception e) {
            LimeLog.warning("Failed to get diagonal inches: " + e.getMessage());
            return 0;
        }
    }

    // 获取设备的PPI值
    public static int getPPI(Context context) {
        try {
            Point screenResolution = getScreenResolution(context);
            int width = screenResolution.x;
            int height = screenResolution.y;

            double diagonalInches = getDiagonalInches(context);
            if (diagonalInches > 0) {
                double diagonalPixels = Math.sqrt(Math.pow(width, 2) + Math.pow(height, 2));
                return (int) (diagonalPixels / diagonalInches);
            }
        } catch (Exception e) {
            LimeLog.warning("Failed to get PPI: " + e.getMessage());
        }
        return context.getResources().getDisplayMetrics().densityDpi;
    }

    // 获取设备的实际屏幕分辨率
    public static Point getScreenResolution(Context context) {
        Point screenResolution = new Point();
        DisplayMetrics realMetrics = new DisplayMetrics();

        WindowManager display = (WindowManager) context.getSystemService(Context.WINDOW_SERVICE);
        if (display != null && display.getDefaultDisplay() != null) {
            display.getDefaultDisplay().getRealMetrics(realMetrics);
            screenResolution.x = realMetrics.widthPixels;
            screenResolution.y = realMetrics.heightPixels;
        } else {
            DisplayMetrics dm = context.getResources().getDisplayMetrics();
            screenResolution.x = dm.widthPixels;
            screenResolution.y = dm.heightPixels;
        }

        return screenResolution;
    }
}
