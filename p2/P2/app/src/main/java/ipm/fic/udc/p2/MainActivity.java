package ipm.fic.udc.p2;


import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.View;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.ListView;
import android.widget.ArrayAdapter;
import java.util.ArrayList;
import java.util.Collections;

import android.content.Intent;
import android.widget.AdapterView;
import android.widget.Toast;
import static java.lang.Boolean.TRUE;


public class MainActivity extends AppCompatActivity {

    /**
     * Atributos
     */

    private static final int IDA = 1;           //Id add
    private static final int IDM = 2;           //Id modify
    private static final int IDS = 3;           //Id sublist

    private static final String LIST = "list";
    private static final String LISTN = "listn";

    private ArrayList<Category> alist = new ArrayList<Category>();          //lista de categorias
    private ArrayList<String> names = new ArrayList<String>();              //lista de nombres de categorias
    private ArrayList<String> categorysublist = new ArrayList<String>();    //lista de elementos de la categoria

    private ArrayAdapter<String> adapter;

    private int categoryselected = 0;
    private String categoryname;
    private String name;

    private Category categoryD = new Category();
    private Category categoryS = new Category();


    /**
     * Metodos
     */

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        this.adapter = new ArrayAdapter<String>(this, android.R.layout.simple_list_item_1, names);

        if (savedInstanceState != null) {
            int i=1;
            while ((names.isEmpty() != TRUE) && (alist.isEmpty()) != TRUE) {
                alist.remove(i);
                names.remove(i);
                i=i+1;
            }
            alist = savedInstanceState.getParcelableArrayList(LIST);
            names.addAll(savedInstanceState.getStringArrayList(LISTN));
        }

        ListView vlist = (ListView) findViewById(R.id.vlist);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        FloatingActionButton fab = (FloatingActionButton) findViewById(R.id.fab);

        vlist.setAdapter(adapter);

        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent eagregar = new Intent(MainActivity.this, MainAddActivity.class);
                eagregar.putStringArrayListExtra("nameslist",names);
                startActivityForResult(eagregar,IDA);
            }
        });


        vlist.setOnItemLongClickListener(new AdapterView.OnItemLongClickListener(){
            @Override
            public boolean onItemLongClick(AdapterView<?> parent, View v, int pos, long id) {
                name = names.get(pos);
                int i = 0;
                categoryname = alist.get(i).getName();

                while (i < alist.size() && (name.compareTo(alist.get(i).getName()) != 0)) {
                    i= i+1;
                }

                categoryname = alist.get(i).getName();
                categorysublist = alist.get(i).getSublist();


                Intent editmodify = new Intent(MainActivity.this, MainEditAndDelete.class);
                editmodify.putExtra("categoryName",categoryname);
                editmodify.putExtra("posAn",pos);
                editmodify.putExtra("posAa",i);
                editmodify.putStringArrayListExtra("categorysublist",categorysublist);
                editmodify.putStringArrayListExtra("nameslist",names);

                startActivityForResult(editmodify,IDM);
                return false;
            }

        });

        vlist.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, int pos, long id) {
                name = names.get(pos);
                int i = 0;
                categoryname = alist.get(i).getName();

                while (i < alist.size() && (name.compareTo(alist.get(i).getName()) != 0)) {
                    i= i+1;
                }

                categorysublist = alist.get(i).getSublist();
                categoryname = alist.get(i).getName();

                Intent sublist = new Intent(MainActivity.this, ShowSubList.class);
                sublist.putExtra("posS",i);
                sublist.putExtra("categoryName",categoryname);
                sublist.putStringArrayListExtra("categorysublist",categorysublist);

                startActivityForResult(sublist,IDS);

            }
        });

    }



    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if(resultCode==RESULT_OK && requestCode==IDA){
            categoryD = data.getParcelableExtra("categoryD");
            if (categoryD.getName().length() != 0) {
                alist.add(categoryD);
                names.add(categoryD.getName());

            }
            Collections.sort(names);
            this.adapter.notifyDataSetChanged();
        }

        if(resultCode==RESULT_OK && requestCode==IDM){
            if (data.getIntExtra("posDa", categoryselected) != -1) {
                alist.remove(data.getIntExtra("posDa", categoryselected));
                names.remove(data.getIntExtra("posDn", categoryselected));
                categoryD = data.getParcelableExtra("categoryD");
                if (categoryD.getName().length() != 0) {
                    alist.add(categoryD);
                    names.add(categoryD.getName());
                }
            }
            Collections.sort(names);
            this.adapter.notifyDataSetChanged();
        }

        if(resultCode==RESULT_OK && requestCode==IDS){
            categoryS = alist.get(data.getIntExtra("categoryS", categoryselected));
            categoryS.setSublist(data.getStringArrayListExtra("sublist"));
            Collections.sort(names);
            this.adapter.notifyDataSetChanged();
        }

    }


    @Override
    public void onSaveInstanceState(Bundle savedInstanceState) {
        savedInstanceState.putParcelableArrayList(LIST, alist);
        savedInstanceState.putStringArrayList(LISTN, names);

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
