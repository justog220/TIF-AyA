#/usr/bin/perl -w
use strict;
use Bio::Tools::GFF;
use Bio::SeqIO::fasta;
use Bio::Seq;


#Manejo argumentos
if (scalar @ARGV != 2)
{
        die "Uso: perl disenio_primers.pl ruta_fasta ruta_gff\n"
}

my $fasta_route = $ARGV[0];
my $gff_route = $ARGV[1];

#-----Leo version GFF----
open(GFFFILE, $gff_route) or die "No se pudo abrir el archivo GFF.\n";

my $primer_linea = <GFFFILE>;
chomp($primer_linea);
my @fields = split(' ', $primer_linea);
my $version = @fields[-1];
#------------------------

my $ruta_salida = 'salida.tsv';
open(SALIDA, '>', $ruta_salida) or die "No se pudo abrir el archivo de salida\n";
print SALIDA "nombre_gen\tsecuencia_fw\tTm_fw\tTa_fw\tsecuencia_rv\tTm_rv\tTa_rv\ttamanio_producto\n";

my $gffio = Bio::Tools::GFF->new(-file => $gff_route, -gff_version =>$version);
my $seqio = Bio::SeqIO->new(-format => 'fasta', -file => $fasta_route);
my $seqout= Bio::SeqIO->new( -format => 'Fasta', -file => '>productos_pcr.fa');
my $seq = $seqio->next_seq();

my $feature;
my @bases = ('A', 'C', 'G', 'T');

use Data::Dumper;

while($feature = $gffio->next_feature())
{
	my @ids = $feature->get_tag_values('ID');
	my $gen = $ids[0];
	# print "Feature for ",$feature->get_tag_values('ID')," starts ",$feature->start," ends ", $feature->end," strand ",$feature->strand," length ",$feature->length,"\n";
	my $inicio = $feature->start;
	my $fin = $feature->end;
	my $seqstr;
	my $seq_fw;
	my $seq_rv;
	if ($feature->strand > 0)
	{
		$seqstr = $seq->trunc($inicio-5, $fin+5)->seq;
		$seq_fw = $seq->trunc($inicio-5, $inicio+14)->seq;
		$seq_fw =~ tr/ACGT/TGCA/;	
		$seq_rv = $seq->trunc($fin-14, $fin+5)->seq;
		$seq_rv = reverse $seq_rv;
	}
	else
	{
		$seqstr = $seq->trunc($inicio-5, $fin+5)->seq;
		$seqstr =~ tr/ACGT/TGCA/;
		$seqstr = reverse $seqstr;
		$seq_fw = $seq->trunc($fin-15, $fin+4)->seq;
		$seq_fw = reverse $seq_fw;
		$seq_rv = $seq->trunc($inicio-5, $inicio+14)->seq;
		$seq_rv =~ tr/ACGT/TGCA/;
	}

	my %conteos_fw;
	my %conteos_rv;
	foreach my $base (@bases){
		my $base_min = lc($base);
		$conteos_fw{$base} = length( $seq_fw =~ s/[^\Q$base\E]//rg ); # Teníamos problemas con como lo habiamos visto en clase y lo solucionamos con: https://stackoverflow.com/questions/34437248/is-there-a-better-way-to-count-occurrence-of-char-in-a-string
		$conteos_rv{$base} = length( $seq_rv =~ s/[^\Q$base\E]//rg );
	}

	# print Dumper(\%conteos_fw);
	# print Dumper(\%conteos_rv);

	my $Tm_fw = 4 * ($conteos_fw{'G'} + $conteos_fw{'C'}) + 2 * ($conteos_fw{'A'} + $conteos_fw{'T'});
	my $Ta_fw = $Tm_fw - 5;
	my $Tm_rv = 4 * ($conteos_rv{'G'} + $conteos_rv{'C'}) + 2 * ($conteos_rv{'A'} + $conteos_rv{'T'});
	my $Ta_rv = $Tm_rv - 5;

	my $tamanio = $feature->length + 10;
	print SALIDA $gen . "\t" . $seq_fw . "\t" . $Tm_fw . "\t" . $Ta_fw . "\t" . $seq_rv . "\t" . $Tm_rv . "\t" . $Ta_rv . "\t" . $tamanio . "\n";

	my $header = $gen . "-" . $tamanio . "bp";	

	my $new_seq = Bio::Seq->new(-seq => $seqstr,
								-id => $header);

	$seqout->write_seq($new_seq)
}

$gffio->close();
$seqio->close();
$seqout->close();
close(SALIDA);