<?php
include($_SERVER['DOCUMENT_ROOT'] ."/manager/includes/connect.php");
$procedur_id=15;
$procedur_idd=9;
$postData = file_get_contents('php://input');
$data = json_decode($postData, true);//iddd=$_GET['id'];
foreach ($data as $iddd=>$views){
//$iddd=4129664;
	$stmt=$dbh->prepare("SELECT `id`,`category`,`price`,`torgi`,`address`,`city`,`current_price` FROM `modx_1_prodazha` WHERE `id`=:iddd");
	$stmt->bindParam(':iddd', $iddd);
	$stmt->execute();
	$rows = $stmt->fetchAll();


	foreach ($rows as $row){
		$category=$row['category'];
		if ($category==17 or $category==50 or $category==28 or $category==44 or $category==26){$category=10;}
		elseif($category==24){$category=7;}
		elseif($category==20){$category=1;}
		elseif($category==21){$category=2;}
		elseif($category==22){$category=3;}
		elseif($category==104){$category=4;}
		elseif($category==61){$category=5;}
		elseif($category==23){$category=6;}
		elseif($category==25){$category=8;}
		elseif($category==106 ){$category=21;}
		elseif($category==75){$category=22;}
		elseif($category==17){$category=23;}
		elseif($category==29){$category=24;}
		elseif($category==19 or $category=29 or $category=30){$category=27;}
		else{continue;}
		$torgi=$row['torgi'];
		$id=$row['id'];
		$c=$row['address'];
		$cc=$row['city'];
		if(strpos($c, 'Моск')!==false or strpos($cc, 'Моск')!==false){
			$city=1;
		}
		else{
			$city=0;
		}
		
		$price=$row['price'];

		if (!empty($price)) {
			// echo "||||||||";
			$stmt1=$dbh->prepare("SELECT `id`,`start_pr`,`end_pr` FROM `modx_range_price` WHERE `start_pr`<= :price AND :price <= `end_pr`");
			$stmt1->bindParam(':price',$price);
			$stmt1->execute();
			$r = $stmt1->fetch(PDO::FETCH_ASSOC);
			$id_pr=$r['id'];
			
			$stmt2=$dbh->prepare("SELECT `param` FROM `modx_calculation` WHERE `id_price`=:id_pr AND `type_torg`=:torgi AND `moscow`=:city AND `category`=:category AND `procedur_id`=:procedur_idd");
			$stmt2->bindParam(':id_pr',$id_pr);
			$stmt2->bindParam(':torgi',$torgi);
			$stmt2->bindParam(':city',$city);
			$stmt2->bindParam(':category',$category);
			$stmt2->bindParam(':procedur_idd',$procedur_idd);
			$stmt2->execute();
			$row1 = $stmt2->fetch(PDO::FETCH_ASSOC);
			
			$param1=$row1['param'];
			$param=str_ireplace(",", ".", $param1);
			
			
			$prognosis1=$price*$param;
			$prognosis=floatval($prognosis1);
			$prognos=$prognosis/5;
		if ($prognos<1){
			$prog=1;
		}
		else{
			$prog=round($prognos)*5;
		}
		
		if(!empty($prognosis)){

			
			if ($torgi==1){
				$stm=$dbh->prepare("SELECT `param` FROM `modx_calculation` WHERE `id_price`=:id_pr AND `type_torg`=:torgi AND `moscow`=:city AND `category`=:category AND `procedur_id`=:procedur_id");
				$stm->bindParam(':id_pr',$id_pr);
				$stm->bindParam(':torgi',$torgi);
				$stm->bindParam(':city',$city);
				$stm->bindParam(':category',$category);
				$stm->bindParam(':procedur_id',$procedur_id);
				$stm->execute();
				$rr=$stm->fetch(PDO::FETCH_ASSOC);
				// echo "Процент покупки по начальной цене-";
				$win_pr_now1=$rr['param'];
				$win_pr_now=round($win_pr_now1,2);
				// print_r($rr['param']);
			}
			$cur_pr=$row['current_price'];
			$current_price=floatval($cur_pr);

			$price=floatval($price);				
			if(!empty($current_price) and !empty($price) and $current_price!=0 and $price!=0 and $torgi==-1){

				if(($current_price-$prognosis)>0)
					$xx=1;
				else
					$xx=-1;

				$win_pr_now1=($xx*pow(abs($current_price-$prognosis),1/3.)+pow($prognosis,1/3.))/(pow(($price-$prognosis),1/3.)+pow($prognosis,1/3.));
				$win_pr_now1=floatval($win_pr_now1*100.);
				$win_pr_now=round($win_pr_now1,2);
				// echo "ПОКУПКА ПО ДАННОЙ ЦЕНЕ";
				// print_r($win_pr_now);

			}
			$s=$dbh->prepare("SELECT `id` FROM `modx_prognoz` WHERE `id`=:id1");
			$s->bindParam(':id1', $id);
			$s->execute();
			$qwe=$s->fetch(PDO::FETCH_ASSOC);
			if(empty($qwe)){
			$stmt3=$dbh->prepare("INSERT INTO `modx_prognoz`(`lot_id`,`prognosis`,`win_procent`) VALUES (:lot_id, :prognosis, :win_procent)");
			$stmt3->bindParam(':lot_id',$id);
			$stmt3->bindParam(':prognosis',$prog);
			$stmt3->bindParam(':win_procent', $win_pr_now);
			$stmt3->execute();
			}
			else{
				$stmtt3=$dbh->prepare("UPDATE `modx_prognoz` SET (`prognosis`=:prognosis,`win_procent`=:win_procent) WHERE `lot_id`=:lot_id");			
				$stmtt3->bindParam(':lot_id',$id);
				$stmtt3->bindParam(':prognosis',$prog);
				$stmtt3->bindParam(':win_procent', $win_pr_now);
				$stmtt3->execute();
			}
			// echo "Город-";
			// print_r($city);	
			// echo "Категория-";
			// print_r($category);
			// echo "Цена-";
			// print_r($price);
			// echo "Торги-";			
			// print_r($torgi);
			// echo("Ценовой id-");
			// print_r($r['id']);
			// echo "Коэфф-";
			// print_r($param);
			// echo "Прогноз-";
			// print_r($prognosis);
			// echo "ДОБАВИЛ!";
			}
		}
	}
}


?>
