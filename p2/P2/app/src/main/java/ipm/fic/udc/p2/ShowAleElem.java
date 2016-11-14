package ipm.fic.udc.p2;


import android.content.Intent;
import android.hardware.SensorManager;
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


public class ShowAleElem extends AppCompatActivity {


    /**
     * Atributos
     */

    private static final int IDAM = 1;

    private static final String RELEM = "Relem";

    private ArrayList<String> rlist = new ArrayList<String>();

    private ArrayAdapter<String> radapterR;

    private TextView txsublist;
    private Button bCancelS;
    private ListView vlist;

    private Bundle extras;
    private int elementselecteds;
    private int elementselectedr;
    private String elementname;
    private String category;

    private String nameEA;
    private boolean editedA = false;


    /**
     * Metodos
     */
    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.show_ale_elem);

        extras = getIntent().getExtras();

        elementselecteds = extras.getInt("posR");
        elementname = extras.getString("elemR");
        category = extras.getString("categoryR");

        this.radapterR = new ArrayAdapter<String>(this, android.R.layout.simple_list_item_1, rlist);

        if (savedInstanceState == null) {
            rlist.add(elementname);
        } else {
            if (rlist.isEmpty()) {
                rlist.add(0, savedInstanceState.getString(RELEM));
            }
        }

        txsublist = (TextView) findViewById(R.id.txTitle);
        txsublist.setText(category);
        vlist = (ListView) findViewById(R.id.sublist);
        bCancelS = (Button) findViewById(R.id.btCancelS);

        vlist.setAdapter(radapterR);

        this.radapterR.notifyDataSetChanged();


        vlist.setOnItemLongClickListener(new AdapterView.OnItemLongClickListener(){
            @Override
            public boolean onItemLongClick(AdapterView<?> parent, View v, int pos, long id) {
                elementselectedr = pos;
                elementname = rlist.get(elementselectedr);

                Intent editmodifyElem = new Intent(ShowAleElem.this, SubEditAndDelete.class);
                editmodifyElem.putExtra("posE",elementselectedr);
                editmodifyElem.putExtra("name",elementname);
                editmodifyElem.putExtra("editedA",editedA);

                startActivityForResult(editmodifyElem,IDAM);
                return false;
            }

        });


        bCancelS.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent();
                if (editedA) {
                    intent.putExtra("editedDA",editedA);
                    intent.putExtra("posR", elementselecteds);
                    intent.putExtra("elementR", nameEA);
                }
                setResult(RESULT_OK,intent);
                finish();
            }
        });

    }


    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if(resultCode==RESULT_OK && requestCode==IDAM){
            editedA = data.getBooleanExtra("editedC",editedA);
            if (data.getIntExtra("posD", elementselectedr) != -1) {
                rlist.remove(data.getIntExtra("posD", elementselectedr));
                nameEA = data.getStringExtra("nameE");
                if (nameEA.length() != 0) {
                    rlist.add(nameEA);
                }
            }
            this.radapterR.notifyDataSetChanged();
        }

    }


    @Override
    public void onSaveInstanceState(Bundle savedInstanceState) {
        savedInstanceState.putString(RELEM, elementname);

        super.onSaveInstanceState(savedInstanceState);
    }


}
