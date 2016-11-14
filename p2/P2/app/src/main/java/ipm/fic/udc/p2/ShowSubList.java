package ipm.fic.udc.p2;


import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.Collections;

import java.util.concurrent.ThreadLocalRandom;
import android.hardware.Sensor;
import android.hardware.SensorManager;
import android.content.Context;


public class ShowSubList extends AppCompatActivity {


    /**
     * Atributos
     */

    private static final int IDSA = 1;
    private static final int IDSM = 2;
    private static final int IDAle = 3;

    private static final String ELIST = "Elist";

    private ArrayList<String> elist = new ArrayList<String>();

    private ArrayAdapter<String> eadapterS;

    private TextView txsublist;
    private Button bAddS;
    private Button bCancelS;
    private ListView vlist;

    private Bundle extras;
    private int categoryselected;
    private String categoryname;
    private int elementselected;
    private String elementname;
    private String nameE;

    private ShakeDetector mShakeDetector;
    private SensorManager mSensorManager;
    private Sensor mAccelerometer;
    private String elementrandom;
    private boolean editedDA = false;

    /**
     * Metodos
     */
    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.show_sublist);

        extras = getIntent().getExtras();

        categoryselected = extras.getInt("posS");
        elist = extras.getStringArrayList("categorysublist");
        categoryname = extras.getString("categoryName");

        this.eadapterS = new ArrayAdapter<String>(this, android.R.layout.simple_list_item_1, elist);

        if (savedInstanceState != null) {
            elist.clear();
            elist.addAll(savedInstanceState.getStringArrayList(ELIST));
        }

        txsublist = (TextView) findViewById(R.id.txTitle);
        txsublist.setText(categoryname);
        vlist = (ListView) findViewById(R.id.sublist);
        bAddS = (Button) findViewById(R.id.btAddS);
        bCancelS = (Button) findViewById(R.id.btCancelS);

        vlist.setAdapter(eadapterS);

        bAddS.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent agregarElem = new Intent(ShowSubList.this, SubAddActivity.class);
                startActivityForResult(agregarElem,IDSA);
            }
        });


        vlist.setOnItemLongClickListener(new AdapterView.OnItemLongClickListener(){
            @Override
            public boolean onItemLongClick(AdapterView<?> parent, View v, int pos, long id) {
                elementselected = pos;
                elementname = elist.get(elementselected);

                Intent editmodifyElem = new Intent(ShowSubList.this, SubEditAndDelete.class);
                editmodifyElem.putExtra("posE",elementselected);
                editmodifyElem.putExtra("name",elementname);

                startActivityForResult(editmodifyElem,IDSM);
                return false;
            }

        });

        bCancelS.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                mSensorManager.unregisterListener(mShakeDetector);

                Intent intent = new Intent();
                intent.putStringArrayListExtra("sublist",elist);
                intent.putExtra("categoryS", categoryselected);
                setResult(RESULT_OK,intent);
                finish();
            }
        });


        mSensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
        mAccelerometer = mSensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);

        if (mAccelerometer != null) {

            mShakeDetector = new ShakeDetector(new ShakeDetector.OnShakeListener() {
                @Override
                public void onShake() {
                    if (elist.isEmpty() != true) {
                        mSensorManager.unregisterListener(mShakeDetector);

                        int posrandom = ThreadLocalRandom.current().nextInt(0, elist.size());

                        elementrandom = elist.get(posrandom);

                        Intent AleatElem = new Intent(ShowSubList.this, ShowAleElem.class);
                        AleatElem.putExtra("posR", posrandom);
                        AleatElem.putExtra("elemR", elementrandom);
                        AleatElem.putExtra("categoryR", categoryname);


                        startActivityForResult(AleatElem, IDAle);
                    }
                }
            });

            mSensorManager.registerListener(mShakeDetector, mAccelerometer, SensorManager.SENSOR_DELAY_UI);
        }
    }


    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if(resultCode==RESULT_OK && requestCode==IDSA){
            nameE = data.getStringExtra("nameE");
            if (nameE.length() != 0) {
                elist.add(nameE);
            }
            Collections.sort(elist);
            this.eadapterS.notifyDataSetChanged();
        }

        if(resultCode==RESULT_OK && requestCode==IDSM){
            if (data.getIntExtra("posD", elementselected) != -1) {
                elist.remove(data.getIntExtra("posD", elementselected));
                nameE = data.getStringExtra("nameE");
                if (nameE.length() != 0) {
                    elist.add(nameE);
                }
            }
            Collections.sort(elist);
            this.eadapterS.notifyDataSetChanged();
        }

        if (resultCode==RESULT_OK && requestCode==IDAle){
            if (data.getBooleanExtra("editedDA",editedDA)) {
                elist.remove(data.getIntExtra("posR", elementselected));
                nameE = data.getStringExtra("elementR");
                if (nameE.length() != 0) {
                    elist.add(nameE);
                }
                Collections.sort(elist);
                this.eadapterS.notifyDataSetChanged();
            }

            mSensorManager.registerListener(mShakeDetector, mAccelerometer, SensorManager.SENSOR_DELAY_UI);
        }

    }


    @Override
    public void onSaveInstanceState(Bundle savedInstanceState) {
        savedInstanceState.putStringArrayList(ELIST, elist);

        super.onSaveInstanceState(savedInstanceState);
    }


}
