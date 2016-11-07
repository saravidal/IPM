package ipm.fic.udc.p2;

import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.View;
import android.view.Menu;
import android.view.MenuItem;
import android.app.Activity;
import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.ArrayAdapter;
import java.util.ArrayList;
import java.util.Collections;

import android.view.View;
import android.content.Intent;
import android.net.Uri;

import android.view.ContextMenu;
import android.view.MenuItem;

import android.widget.AdapterView;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {

    private static final String LIST = "list";
    final ArrayList<String> alist = new ArrayList<String>();
    private ListView vlist;

    private EditText editable;

    private Button badd;
    private Button bcancel;
    private Button bdelete;

    private Boolean editing = false;
    private int itemselected;


    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        final ArrayAdapter<String> adapter = new ArrayAdapter<String>(this,android.R.layout.simple_list_item_1,alist);

        if (savedInstanceState != null)
            alist.addAll(savedInstanceState.getStringArrayList(LIST));

        editable = (EditText) findViewById(R.id.editable);
        badd = (Button) findViewById(R.id.badd);
        bcancel = (Button) findViewById(R.id.bcancel);
        bdelete = (Button) findViewById(R.id.bdelete);
        vlist = (ListView) findViewById(R.id.vlist);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        FloatingActionButton fab = (FloatingActionButton) findViewById(R.id.fab);


        vlist.setAdapter(adapter);


        badd.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view){
                if (editing) {
                    alist.remove(itemselected);
                    editing = false;
                }
                alist.add(editable.getText().toString());
                Collections.sort(alist);
                adapter.notifyDataSetChanged();
                editable.setText("");
                badd.setVisibility(View.GONE);
                bdelete.setVisibility(View.GONE);
                bcancel.setVisibility(View.GONE);
                editable.setVisibility(View.GONE);
            }

        });

        bdelete.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view){
                if (editing) {
                    alist.remove(itemselected);
                    editing = false;
                }
                Collections.sort(alist);
                adapter.notifyDataSetChanged();
                editable.setText("");
                badd.setVisibility(View.GONE);
                bdelete.setVisibility(View.GONE);
                bcancel.setVisibility(View.GONE);
                editable.setVisibility(View.GONE);
            }

        });

        bcancel.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view){
                editable.setText("");
                badd.setVisibility(View.GONE);
                bdelete.setVisibility(View.GONE);
                bcancel.setVisibility(View.GONE);
                editable.setVisibility(View.GONE);
            }

        });

        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                badd.setVisibility(View.VISIBLE);
                editable.setVisibility(View.VISIBLE);
                bdelete.setVisibility(View.GONE);
                bcancel.setVisibility(View.VISIBLE);
            }
        });


        vlist.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int pos, long id) {
                itemselected = pos;
                editing = true;
                editable.setText(alist.get(itemselected));
                badd.setVisibility(View.VISIBLE);
                bdelete.setVisibility(View.VISIBLE);
                editable.setVisibility(View.VISIBLE);
                bcancel.setVisibility(View.VISIBLE);

            }
        });

    }



    @Override
    public void onSaveInstanceState(Bundle savedInstanceState){
        savedInstanceState.putStringArrayList(LIST, alist);
        super.onSaveInstanceState(savedInstanceState);
    }



    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_help) {
            Toast.makeText(getApplicationContext(),
                    R.string.help_toast, Toast.LENGTH_LONG).show();
            return true;
        }

        return super.onOptionsItemSelected(item);
    }



}
